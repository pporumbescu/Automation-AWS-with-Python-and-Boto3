import boto3
import schedule
import time


def create_volume_snapshots(region, tags=None):
    """
    Creates snapshots for EC2 volumes in the specified region, filtered by tags (optional).

    Args:
        region (str): The AWS region where the volumes are located.
        tags (dict, optional): A dictionary of tags to filter the volumes. Defaults to None.
    """
    # Create an EC2 resource object for the specified region
    ec2 = boto3.resource('ec2', region_name=region)

    # Create a list to store the filters
    filters = []

    # If tags are provided, add them to the filters list
    if tags:
        for key, value in tags.items():
            filters.append({'Name': f'tag:{key}', 'Values': [value]})

    # Get all volumes in the specified region, filtered by tags (if provided)
    volumes = ec2.volumes.filter(Filters=filters)

    # Iterate over each volume
    for volume in volumes:
        try:
            # Create a snapshot of the volume
            snapshot = volume.create_snapshot()
            print(f"Created snapshot: {snapshot.id} for volume {volume.id}")
        except Exception as e:
            # If an exception occurs, print an error message with the volume ID and exception details
            print(f"Error creating snapshot for volume {volume.id}: {str(e)}")


# Specify the AWS region where your EC2 instance is located
region = 'us-east-1'

# Optional: Specify tags to filter volumes (e.g., {'Environment': 'Production'})
tags = {'env': 'prod'}

# Schedule the script to run once a day at midnight
schedule.every().day.at("00:00").do(create_volume_snapshots, region=region, tags=tags)

# Run the scheduled tasks indefinitely
while True:
    # Check if any scheduled tasks are pending and run them
    schedule.run_pending()

    # Pause the script for 1 second before checking for pending tasks again
    time.sleep(1)