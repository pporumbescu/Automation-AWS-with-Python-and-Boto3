import boto3
from datetime import datetime, timezone

def list_and_delete_snapshots(region, age_threshold_days, tag_key=None, tag_value=None):
    ec2 = boto3.client('ec2', region_name=region)
    filters = [{'Name': 'owner-id', 'Values': ['self']}]

    # Add tag filter only if both tag_key and tag_value are provided
    if tag_key and tag_value:
        filters.append({'Name': f'tag:{tag_key}', 'Values': [tag_value]})

    try:
        snapshots_response = ec2.describe_snapshots(Filters=filters)
        snapshots = snapshots_response.get('Snapshots', [])
        now = datetime.now(timezone.utc)

        if snapshots:
            print(f"Found {len(snapshots)} snapshots in {region}:")
            for snapshot in snapshots:
                snapshot_id = snapshot['SnapshotId']
                start_time = snapshot['StartTime']
                snapshot_age_days = (now - start_time).days
                # Print snapshot details
                print(f"Snapshot ID: {snapshot_id}, Age: {snapshot_age_days} days, Region: {region}")

                # Delete snapshots older than specified days
                if snapshot_age_days > age_threshold_days:
                    # Uncomment below line to enable deletion
                    # ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(f"Deleted snapshot {snapshot_id} aged {snapshot_age_days} days in {region}.")
        else:
            print(f"No snapshots found in {region} matching the criteria.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
regions = ['us-east-1', 'eu-west-1']
for region in regions:
    list_and_delete_snapshots(region, 30, tag_key='Project', tag_value='MyProject')
