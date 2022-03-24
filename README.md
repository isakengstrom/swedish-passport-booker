# Passport Appointment Booker

> **Note:** Running this script is at your **OWN RISK**. At the time of creating it, nothing has been issued about it being illegal, but it has been described as morally reprehensible, see [source](https://www.svt.se/nyheter/lokalt/stockholm/svart-att-fa-tid-for-nytt-pass-i-stockholm-sa-fick-han-tid-snabbare?fbclid=IwAR2r1q1NWRMq20tXuznfwP69LtV1La3B4-B96FLu0RXp1bMHQoP93MC-fls).    


This Booker takes the booking ID and Email address of an already existing booking, and tries to renew it. The way the website is designed, this method requires less navigation on the website, compared to booking from scratch. The booker only looks in the region that you first booked your appointment, but can handle multiple expeditions in said region (at least up to 4 expeditions are confirmed to work). 

E.g. if you have a booked time in the *Stockholm* region, at the *Solna* expedition. Then you can also search for appointments in *Sthlm City* and *Sollentuna*, but not in *Norrköping*, or *Linköping*        

## Getting started 
This is a Python Azure Functions project. If you know how to get it started, you can run the booker as either an HttpTrigger, or a TimerTrigger. Otherwise, you can create a new python file and call the booker from there.  

> **Note:** Make sure to not ping the website at too high a speed, if running the booker in a loop. Setting up wait statements is a good idea.
You'll need to change  

Have a look in the [config.py](/src/config.py) to see all the settings you'll need to set up. This will also guide you to the [local.settings.example.json](/src/local.settings.example.json), which will need to be filled in and renamed to *local.settings.json* if you're running the booker as an Azure Functions project.  If you're not running it in this way, you'll need to get the environment variables into the runtime in some other way. 

### TimerTrigger
To run the TimerTrigger, you first need to start the Storage Emulator. If you have it installed, you can start it up with the following commands (on windows):  
```cmd
"%programfiles(x86)%\Microsoft SDKs\Azure\Storage Emulator\AzureStorageEmulator.exe" init
"%programfiles(x86)%\Microsoft SDKs\Azure\Storage Emulator\AzureStorageEmulator.exe" start
```
