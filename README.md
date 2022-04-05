# Passport Appointment Booker (Somewhat deprecated)
**With recent updates to [The booking site](https://bokapass.nemoq.se/Booking/Booking/Index/stockholm), it's made quite clear that they don't want scripts/bots to book appointments (by them adding CAPTCHAs and other things..). With that said, this script's focus is a bit niche compared to others I've seen. Compared to booking a new appointment from scratch, this script works by RE-BOOKING an already (manually) booked appointment, requiring fewer clicks (for Selenium) and no bypassing of CAPTCHAs. So if you can circumvent the other blockers on the site, this might be a good option for you. However, as the script has fulfilled its purpose, together with the morally gray area of this whole ordeal, no further updates will be provided. Feel free to use this however you'd like though (under the terms of the MIT licence).**     

> **Note:** Running this script is at your **OWN RISK**. At the time of creating it, nothing has been issued about it being illegal, but it has been described as morally reprehensible by the police, see [source](https://www.svt.se/nyheter/lokalt/stockholm/svart-att-fa-tid-for-nytt-pass-i-stockholm-sa-fick-han-tid-snabbare?fbclid=IwAR2r1q1NWRMq20tXuznfwP69LtV1La3B4-B96FLu0RXp1bMHQoP93MC-fls). For your own sake, make sure to be updated on what the police say, and the terms of service on the site.      

## Other projects:
You are probebly better off trying one of the following solutions:
- [pass-fur-alle](https://github.com/jonkpirateboy/Pass-fur-alle) by @jonkpirateboy
- [passport-appointment-bot](https://github.com/kalkih/passport-appointment-bot) by @kalkih
- [passport_booker_se](https://github.com/elias123tre/passport_booker_se) by @elias123tre

---
## How it works

All of the booking logic can be found in [booker.py](/src/booker.py). This Booker takes the booking ID and Email address/phone number of an **already existing booking**, and tries to renew it. The way the website is designed, this method requires less navigation once a free appointment has been found, compared to booking from scratch.

### Booking location 
The booker only looks in the region that you first booked your appointment, but can handle multiple expeditions in said region (at least up to 4 expeditions are confirmed to work before you get timed out). 

E.g. if you have a booked time in the *Stockholm* region, at the *Solna* expedition, you could also search for appointments in *Sthlm City* and *Sollentuna*, but not in *Norrköping*, or *Linköping*, as they are in *Ostergotland* region.        

### Booking dates
To allow for some further flexibility, min and max date limits can be set, as well as the number of days in foresight from the today's date.  

### Notifications
Once a new booking goes through, the booking site conveniently sends out notifications by itself to your booking email and/or phone number. However, if this is not enough, this script implements another way of sending email notifications to whatever email you'd like.  

## Getting started
There are a few steps needed in order to get started:

### 1. Running the project
This is a Python Azure Functions project. If you know how to get it started, you can run the booker locally, as either an ```HttpTrigger```, or a ```TimerTrigger```. Otherwise, you can create a new python file and call the booker from there in any shape or form you'd like.  

> **Note:** Make sure to not ping the website at too high a speed. Setting up wait statements is a good idea!

Have a look in the [config.py](/src/config.py) to see all the settings you'll need to set up. This will also guide you to the [local.settings.example.json](/src/local.settings.example.json) file, which will need to be filled in and renamed to *local.settings.json* if you're running the booker as an Azure Functions project. If you're not running it in this way, you'll need to get the environment variables into the runtime in some other way. 

You'd also need to install the packages in [requirements.txt](/src/requirements.txt), preferably in a virtual or Conda environment. 

### 2. Book an arbitrary appointment manually 
The first thing you need is an appointment in your wanted region. So go ahead and book any currently available slot.

### 3. Start the script
Run the script until it has renewed your arbitrary appointment into the acceptable date range.  

---
If you want to know more about the ```TimerTriggers```, have a look [here](/src/timer-booker/readme.md).
