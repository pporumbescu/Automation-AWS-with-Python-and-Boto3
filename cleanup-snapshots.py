import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timezone, timedelta
import schedule
import time


def delete_old_snapshots(region, days_old, tag_key=None, tag_value=None):
    # Initialize the EC2 client for the specified AWS region
    ec2_client = boto3.client('ec2', region_name=region)

    # Get the current time in UTC
    now = datetime.now(timezone.utc)

    # Start with a basic filter for snapshots owned by 'self'
    filters = [{'Name': 'owner-id', 'Values': ['self']}]

    # If tag_key and tag_value parameters are provided, add them to the filters
    if tag_key and tag_value:
        filters.append({'Name': f'tag:{tag_key}', 'Values': [tag_value]})

    # Retrieve the snapshots based on the filters
    snapshots = ec2_client.describe_snapshots(Filters=filters)

    # Log the total number of snapshots found
    print(f"Found {len(snapshots['Snapshots'])} snapshots in region {region}.")

    # Iterate through the list of snapshots
    for snap in snapshots['Snapshots']:
        # Calculate how old the snapshot is
        age = now - snap['StartTime']
        # Log details about the snapshot
        print(f"Snapshot ID: {snap['SnapshotId']} | Age: {age.days} days | Region: {region}")
        # If the snapshot is older than the days_old threshold, delete it
        if age > timedelta(days=days_old):
            try:
                # Attempt to delete the snapshot
                response = ec2_client.delete_snapshot(SnapshotId=snap['SnapshotId'])
                # Log the deletion of the snapshot
                print(f"Deleted snapshot {snap['SnapshotId']} aged {age.days} days in region {region}.")
            except ClientError as error:
                # If an error occurs, log it
                print(f"Failed to delete snapshot {snap['SnapshotId']} in region {region}: {error}")


def job():
    # Print a log message when the job starts
    print("Running snapshot cleanup job...")
    # Specify the regions and call delete_old_snapshots for each region
    for region in ['eu-west-1', 'us-east-1']:
        delete_old_snapshots(region, 30, tag_key='Project', tag_value='MyProject')


# Schedule the job to run daily at 3 AM
schedule.every(5).seconds.do(job)

# Keep the script running and check for scheduled jobs
while True:
    schedule.run_pending()
    # Sleep for a short time to prevent the loop from consuming too much CPU
    time.sleep(1)
