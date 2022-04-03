# Passport Appointment Booker (DEPRECATED)

**The maintainers of the booking website have been rolling out a few updates, resulting in breakage of this novel script. As the script has already served it's purpose for me and a handful of acquaintances, no further attempts to bypass these updates will be attempted. But you're welcome to have a go at it yourself if you'd like, see info about the project below**

---
> **Note:** Running this script is at your **OWN RISK**. At the time of creating it, nothing has been issued about it being illegal, but it has been described as morally reprehensible by the police, see [source](https://www.svt.se/nyheter/lokalt/stockholm/svart-att-fa-tid-for-nytt-pass-i-stockholm-sa-fick-han-tid-snabbare?fbclid=IwAR2r1q1NWRMq20tXuznfwP69LtV1La3B4-B96FLu0RXp1bMHQoP93MC-fls).    

## How it works

This Booker takes the booking ID and Email address/phone number of an **already existing booking**, and tries to renew it. The way the website is designed, this method requires less navigation once a free appointment has been found, compared to booking from scratch.

### Booking location 
The booker only looks in the region that you first booked your appointment, but can handle multiple expeditions in said region (at least up to 4 expeditions are confirmed to work before you get timed out). 

E.g. if you have a booked time in the *Stockholm* region, at the *Solna* expedition. Then you can also search for appointments in *Sthlm City* and *Sollentuna*, but not in *Norrköping*, or *Linköping*, as they are in *Ostergotland*        

### Booking dates
To allow for some further flexibility, min and max date limits can be set, as well as the number of days in foresight from the current date.  

### Notifications
Once a new booking goes through, the booking site conveniently sends out notifications by itself to your booking email and/or phone number. However, if this is not enough, this script implements another way of sending email notifications to whatever email you'd like.  

## Getting started
There are a few steps needed in order to get started:

### 1. Running the project
This is a Python Azure Functions project. If you know how to get it started, you can run the booker locally, as either an ```HttpTrigger```, or a ```TimerTrigger```. Otherwise, you can create a new python file and call the booker from there in any shape or form you'd like.  

> **Note:** Make sure to not ping the website at too high a speed if running the booker in a loop. Setting up wait statements is a good idea.

Have a look in the [config.py](/src/config.py) to see all the settings you'll need to set up. This will also guide you to the [local.settings.example.json](/src/local.settings.example.json) file, which will need to be filled in and renamed to *local.settings.json* if you're running the booker as an Azure Functions project. If you're not running it in this way, you'll need to get the environment variables into the runtime in some other way. All of the booking logic can be found in [booker.py](/src/booker.py) 

You'd also need to install the packages in [requirements.txt](/src/requirements.txt), preferably in a virtual or Conda environment. 

### 2. Book an arbitrary appointment 
The first thing you need is an appointment in your wanted region. So go ahead and book any currently available slot.

### 3. Start the script
Run the script until it has renewed your arbitrary appointment into the acceptable date range.  



---
If you want to know more about the ```TimerTriggers```, have a look [here](/src/timer-booker/readme.md).
