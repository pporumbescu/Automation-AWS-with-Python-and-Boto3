import boto3
from datetime import datetime, timezone

def list_snapshots(region):
    # Create an EC2 client for the specified region
    ec2 = boto3.client('ec2', region_name=region)

    try:
        # Retrieve all snapshots owned by the current account
        snapshots_response = ec2.describe_snapshots(OwnerIds=['self'])
        snapshots = snapshots_response.get('Snapshots', [])

        # Get the current timestamp in UTC
        now = datetime.now(timezone.utc)
        print(f"Listing snapshots in {region}:")
        for snapshot in snapshots:
            # Get the start time of the snapshot
            start_time = snapshot['StartTime']
            # Calculate the age of the snapshot in days
            snapshot_age_days = (now - start_time).days
            # Get the tags associated with the snapshot
            tags = snapshot.get('Tags', [])
            # Print the snapshot details
            print(f"Snapshot ID: {snapshot['SnapshotId']} | Region: {region} | Tags: {tags} | Age (days): {snapshot_age_days}")
    except Exception as e:
        # Print an error message if an exception occurs while listing snapshots
        print(f"An error occurred while listing snapshots in {region}: {e}")

def delete_old_snapshots(region, tag_key=None, tag_value=None):
    # Create an EC2 client for the specified region
    ec2 = boto3.client('ec2', region_name=region)

    try:
        # Retrieve all snapshots owned by the current account
        snapshots_response = ec2.describe_snapshots(OwnerIds=['self'])
        snapshots = snapshots_response.get('Snapshots', [])

        # Get the current timestamp in UTC
        now = datetime.now(timezone.utc)
        # Filter snapshots older than or equal to 0 days and with the specified tag (if provided)
        snapshots_to_delete = [snapshot['SnapshotId'] for snapshot in snapshots
                               if (now - snapshot['StartTime']).days > 30
                               and (tag_key is None or all(tag.get('Key') == tag_key and tag.get('Value') == tag_value for tag in snapshot.get('Tags', [])))]

        for snapshot_id in snapshots_to_delete:
            # Delete each snapshot individually
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Deleted snapshot {snapshot_id} in {region}")

        print(f"Deleted {len(snapshots_to_delete)} snapshots in {region} older than 30 days with the specified tag.")
    except Exception as e:
        # Print an error message if an exception occurs while processing snapshots
        print(f"An error occurred while processing {region}: {e}")

# List of regions to process
regions = ['us-east-1', 'eu-west-1']  # Add more regions as needed
# Tag key for filtering snapshots (optional)
tag_key = 'Environment'  # Specify the tag key for filtering (optional)
# Tag value for filtering snapshots (optional)
tag_value = 'Production'  # Specify the tag value for filtering (optional)

# Iterate over each region
for region in regions:
    # List all snapshots in the region
    list_snapshots(region)
    # Delete snapshots older than or equal to 0 days with the specified tag in the region
    delete_old_snapshots(region, tag_key, tag_value)