import smtplib
import logging
import os
from typing import List
from email.message import EmailMessage



def send_booking_update_email(new_booked:str, prev_booked:str, new_expedition: str, prev_expedition:str, bookingId:str, bookingEmail:str, notificationEmails: List[str]):
    try:
        from_email_address = os.environ['devEmailAddress']
        from_email_password = os.environ['devEmailPassword']
        
        msg = EmailMessage()

        msg['Subject'] = f"New booking slot in {new_expedition}: {new_booked}"
        msg['From'] = from_email_address
        msg['To'] = notificationEmails
        msg.set_content(f"The booking was updated from {prev_booked} in {prev_expedition}, to {new_booked} in {new_expedition}. \n\nID: {bookingId}, Email: {bookingEmail}.")

        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(from_email_address, from_email_password)

        server.send_message(msg)
        server.close()
    except:
        logging.error("Exception when sending email alert..")
        raise