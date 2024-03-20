import requests
import smtplib
import os
import schedule
import time

# Retrieve email address and password from environment variables
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


def send_notification(email_msg):
    """
    Sends an email notification with the provided message.
    """
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        msg = f"Subject: Application is down\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)


def check_website():
    """
    Checks the status of the website and sends a notification if it's down or inaccessible.
    """
    try:
        # Send a GET request to the website
        response = requests.get('https://petrucloudss.com/')

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            print('Application is running successfully')
        else:
            print('Application is down. Fix it!')
            msg = f"Application returned: {response.status_code}"
            send_notification(msg)

    except Exception as ex:
        # Handle any exceptions that occur during the request
        print(f'Connection error happened: {ex}')
        msg = "Not accessible!"
        send_notification(msg)

check_website()

# # Schedule the website check to run every 1 hour
# schedule.every(1).hours.do(check_website)
#
# while True:
#     # Run pending scheduled tasks
#     schedule.run_pending()
#
#     # Wait for 1 second before the next iteration
#     time.sleep(1)
