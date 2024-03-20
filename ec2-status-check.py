import boto3
import schedule
import logging
import time
import os
from botocore.exceptions import ClientError, BotoCoreError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Retrieve the AWS region from an environment variable or default to a specific region
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')

# Initialize boto3 client for a specific region
ec2_client = boto3.client('ec2', region_name=AWS_REGION)


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

                # Implement your notification logic here if instance or system status is not 'ok'
                # ...

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
    # Perform any cleanup here if necessary