import os

CONFIG:dict = {
    # Your booking ID and Email 
    # See local.settings.example.json
    "bookingId": os.environ["bookingId"],
    "bookingEmail": os.environ["bookingEmail"], 

    # The first date you're able to book
    "bookingStartDate": "2022-03-18", 

    # The deadline, the last possible date for a booking  
    "bookingEndDate": "2022-05-15", 

     # How many days ahead from today is the booking allowed
    "bookingForesight": 7,

    # The region you already have an appointment in
    # E.g: "stockholm" or "ostergotland"
    "bookingCounty": "stockholm", 

    # List of expeditions you are willing to travel to. 
    # Limited to your region. 
    # Case sensitive
    # E.g: ["Norrköping", "Linköping"] or ["Solna", "Sthlm City", "Sollentuna"]
    "bookingExpeditions": ["Solna", "Sthlm City", "Sollentuna"], 

    # Website URL
    "URL": "https://bokapass.nemoq.se/Booking/Booking/Index/", 

    # Do you want separate email notifications, other than the ones that are sent from the website itself? 
    # Requires additional setup (see local.settings.example.json) 
    "sendNotificationEmail": False, 
    "notificationEmails": ["<YOUR_NOTIFICATION_EMAIL_HERE>", "<YOUR_OTHER_NOTIFICATION_EMAIL_HERE>"] 
} 