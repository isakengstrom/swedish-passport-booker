from contextlib import contextmanager
from enum import Enum
import logging
from datetime import datetime, timedelta 
import os
import random
import time
from typing import List
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from email_alert import send_booking_update_email

def is_valid_date(compare_date:datetime, current_date:datetime, min_date:datetime, max_date:datetime, foresight:int) -> bool:
    return is_post_forsight(compare_date, foresight) and is_in_specified_date_limit(compare_date,min_date,max_date) and is_earlier_than_currently_booked(compare_date,current_date)

def is_in_specified_date_limit(compare_date:datetime, min_date:datetime, max_date:datetime) -> bool:
    return min_date < compare_date < max_date

def is_earlier_than_currently_booked(compare_date:datetime, current_date: datetime) -> bool:
    return compare_date < current_date

def is_post_forsight(compare_date:datetime, foresight: int) -> bool:
    return datetime.today().date() + timedelta(days=foresight) < compare_date.date()

@contextmanager
def driver_context():
    options = Options()

    # Running headless means there is no browser window 
    options.headless = False
    
    # Add this disable option to remove basic detection of a webdriver
    options.add_argument("--disable-blink-features")
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(os.environ["CHROMEWEBDRIVER"], options=options)

    try:
        yield driver
    finally:
        driver.quit()


def booker(config:dict) -> None:    
    try:
        start = time.time()
        time.sleep(random.uniform(0.02, .1))
        timeout = 5
        max_wait_for_load = 1


        # Date formats
        datetime_format = '%Y-%m-%d %H:%M'
        datetime_format_long = '%Y-%m-%d %H:%M:%S'
        date_format = '%Y-%m-%d'

        start_date = datetime.strptime(config["bookingStartDate"], date_format)
        end_date = datetime.strptime(config['bookingEndDate'], date_format)

        booking_id = config["bookingId"]
        booking_email = config["bookingEmail"]

        with driver_context() as driver:
            driver.implicitly_wait(timeout)
            
            full_url = f"{config['URL']}{config['bookingCounty']}"

            # get website and wait for its elements to load
            driver.get(full_url)
            booking_number_xpath = '//input[@id="BookingNumber"]'

            driver.implicitly_wait(0.3)
            WebDriverWait(driver, max_wait_for_load).until(EC.visibility_of_element_located((By.XPATH, booking_number_xpath)))
            driver.implicitly_wait(timeout)

            # Fill in re-booking forms and click to login
            driver.find_element_by_xpath(booking_number_xpath).send_keys(booking_id)
            driver.find_element_by_xpath('//input[@id="ContactInfo"]').send_keys(booking_email)

            driver.find_element_by_xpath('//input[@name="NextButtonID6"]').click()

            # Paths to Currently booked information
            booked_time_xpath = '//label[@for="BookedDateTime"]/parent::div/child::div[@class="controls"]/child::span[@class="control-freetext"]'
            booked_expedition_xpath = '//label[@for="BookedSectionName"]/parent::div/child::div[@class="controls"]/child::span[@class="control-freetext"]'
            
            # Wait for login
            driver.implicitly_wait(0.4)
            WebDriverWait(driver, max_wait_for_load).until(EC.visibility_of_element_located((By.XPATH, booked_time_xpath)))
            driver.implicitly_wait(timeout)

            # Extract the currently booked datetime 
            booked_time:str = driver.find_element_by_xpath(booked_time_xpath).text
            currently_booked_datetime:datetime = datetime.strptime(booked_time, datetime_format)
            
            # Extract the currently booked expedition
            booked_expedition_name:str = driver.find_element_by_xpath(booked_expedition_xpath).text

            # Click to move to, and then wait for booking page to load 
            driver.find_element_by_xpath('//input[@name="NextButtonID26"]').click()
            first_free_time_xpath = '//input[@name="TimeSearchFirstAvailableButton"]'

            driver.implicitly_wait(3)
            WebDriverWait(driver, max_wait_for_load).until(EC.visibility_of_element_located((By.XPATH, first_free_time_xpath)))
        
            expedition_select_xpath = f"//select[@data-provider='#RegionId']"
            
            for expedition in config["bookingExpeditions"]:
                driver.implicitly_wait(0.1)
                select:Select = Select(driver.find_element_by_xpath(expedition_select_xpath))
                driver.implicitly_wait(timeout)

                # Select the correct expedition 
                if expedition == "current":
                    expedition = select.first_selected_option.text
                else:
                    available_expeditions = [(o.text) for o in select.options] 
                    if expedition in available_expeditions:
                        select.select_by_visible_text(expedition)

                # Clicks element to load the earliest available times, then wait for the earliest elements to load 
                driver.find_element_by_xpath(first_free_time_xpath).click()
                try:
                    WebDriverWait(driver, max_wait_for_load).until(EC.presence_of_element_located((By.XPATH, f"//input[@id='datepicker' and not(@value='{currently_booked_datetime.strftime(date_format)}')]")))
                except TimeoutException as e:
                    pass

                driver.implicitly_wait(1)
                time_cells: List[WebElement] = driver.find_elements_by_xpath('//div[@data-function="timeTableCell" and not(@aria-label="Bokad")]') 
        
                if not time_cells:
                    continue

                first_time_cell = time_cells[0]
                earliest_available = first_time_cell.get_attribute("aria-label")

                found_datetime = datetime.strptime(earliest_available, datetime_format_long)
                        
                if is_valid_date(found_datetime, currently_booked_datetime, start_date, end_date, config["bookingForesight"]):
                    first_time_cell.click()
                    driver.find_element_by_xpath('//input[@id="booking-next"]').click()
                    
                    WebDriverWait(driver, max_wait_for_load).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='EmailAddress']")))
                    logging.warning(f"Re-booked to: {earliest_available} at {expedition}")
                    
                    if config["sendNotificationEmail"]:
                        notificationEmails = config["notificationEmails"]
                        send_booking_update_email(earliest_available, booked_time, expedition, booked_expedition_name, booking_id, booking_email, notificationEmails)
                    
                    break

                end = time.time()
                logging.info(f"Booked: {booked_time} in {booked_expedition_name} | First un-booked: {earliest_available} in {expedition} | execution time: {end-start:.1f}s")
                start = time.time()
                time.sleep(random.uniform(0.01, .15))
           
    except TimeoutException as e: 
        logging.exception(f"A Selenium TimeoutException occurred: {e}")
    except Exception as e:
        logging.exception(f"An exception occurred: {e}")