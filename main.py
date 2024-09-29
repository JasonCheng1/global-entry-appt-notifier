#!/usr/bin/env python

import requests
import time
import sys
from datetime import datetime, timedelta
import subprocess

PHONE_NO = "" # TODO import from .env
OASSCRIPT_TEMPLATE = f"""osascript -e 'tell application "Messages" to send "{{message}}" to buddy "{{phone_no}}"'"""


# API URL
APPOINTMENTS_URL = "https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=1&locationId={}&minimum=1"

# List of Global Entry locations
# REF: https://ttp.cbp.dhs.gov/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true&serviceName=Global%20Entry
# REF: https://github.com/Drewster727/goes-notify?tab=readme-ov-file#goes-center-codes
LOCATION_IDS = {
    # 'ARIZONA': 5007,
    'PHILLY': 5445,
    "O'Hare": 5183
}

# How often to run this check in seconds
TIME_WAIT = 300

# Number of days into the future to look for appointments
DAYS_OUT = 10

# Dates
now = datetime.now()
future_date = now + timedelta(days=DAYS_OUT)


def send_text(message: str, phone_no: int = PHONE_NO) -> None:
    cmd = OASSCRIPT_TEMPLATE.format(message=message, phone_no=phone_no)
    subprocess.run(cmd, shell=True)
    print(message, "Sent text successfully! {}".format(cmd))

def check_appointments(city, id):
    url = APPOINTMENTS_URL.format(id)
    appointments = requests.get(url).json()
    return appointments

def appointment_in_timeframe(now, future_date, appointment_date):
    if now <= appt_datetime <= future_date:
        return True
    else:
        return False


try:
    while True:
        for city, id in LOCATION_IDS.items():
            try:
                appointments = check_appointments(city, id)
            except Exception as e:
                print("Could not retrieve appointments from API.")
                appointments = []

            if appointments:
                appt_datetime = datetime.strptime(appointments[0]['startTimestamp'], '%Y-%m-%dT%H:%M')

                if appointment_in_timeframe(now, future_date, appt_datetime):
                    message = "{}: Found an appointment at {}!".format(city, appointments[0]['startTimestamp'])
                    try:
                        send_text(message=message)
                        # sms_sid = send_text(TEXT_TO_NUMBER, TEXT_FROM_NUMBER, message, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                        
                    except Exception as e:
                        print(e)
                        print(message, "Failed to send text")
                else:
                    print("{}: No appointments during the next {} days.".format(city, DAYS_OUT))
            else:
                print("{}: No appointments during the next {} days.".format(city, DAYS_OUT))
            time.sleep(1)
        time.sleep(TIME_WAIT)
except KeyboardInterrupt:
    sys.exit(0)