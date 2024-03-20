import boto3
import schedule
import logging
import smtplib
import time
import os
from botocore.exceptions import ClientError, BotoCoreError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Retrieve the AWS region from an environment variable or default to a specific region
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')

# Initialize boto3 client for a specific region
ec2_client = boto3.client('ec2', region_name=AWS_REGION)

# Retrieve email address and password from environment variables
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


def send_notification(instance_id, status_type, status):
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            subject = f"Instance {instance_id} - {status_type} Status: {status}"
            body = f"Instance {instance_id} has {status_type} status: {status}. Please check the instance."
            msg = f"Subject: {subject}\n\n{body}"
            smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)
            logging.info(f"Email notification sent for instance {instance_id}")
    except smtplib.SMTPAuthenticationError as e:
        logging.error(f"SMTP authentication error: {e}")
    except Exception as e:
        logging.error(f"An error occurred while sending email: {e}")


def check_instance_status():
    try:
        # Describe all instances' status in the specified region
        paginator = ec2_client.get_paginator('describe_instance_status')
        page_iterator = paginator.paginate(IncludeAllInstances=True)

        for page in page_iterator:
            for status in page.get('InstanceStatuses', []):
                instance_id = status.get('InstanceId', 'N/A')
                ins_status = status['InstanceStatus'].get('Status', 'N/A')
                sys_status = status['SystemStatus'].get('Status', 'N/A')
                state = status['InstanceState'].get('Name', 'N/A')
                logging.info(
                    f"Instance {instance_id} in region {AWS_REGION} is {state} with instance status {ins_status} and system status {sys_status}")

                # Send notification if instance or system status is not 'ok'
                if ins_status != 'ok':
                    send_notification(instance_id, "Instance", ins_status)
                if sys_status != 'ok':
                    send_notification(instance_id, "System", sys_status)

    except (ClientError, BotoCoreError) as e:
        logging.error(f"An AWS error occurred: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


# Schedule the function to run every 5 seconds (or use a configurable interval)
schedule.every(5).seconds.do(check_instance_status)

try:
    # Run the schedule as long as the script is running
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    logging.info("Script was terminated by the user")