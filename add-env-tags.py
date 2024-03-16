import boto3
from botocore.exceptions import ClientError


# Define a function to tag instances with multiple tags
def tag_instances(ec2_client, ec2_resource, region, tags):
    try:
        # Retrieve the IDs of all instances
        instance_ids = []
        reservations = ec2_client.describe_instances()['Reservations']
        for res in reservations:
            instances = res['Instances']
            for ins in instances:
                instance_ids.append(ins['InstanceId'])

        # Only attempt to tag if instance IDs are found
        if instance_ids:
            response = ec2_resource.create_tags(
                Resources=instance_ids,
                Tags=tags
            )
            print(f"Instances in {region} have been tagged with {tags}")
        else:
            print(f"No instances to tag in {region}")
    except ClientError as e:
        print(f"An error occurred: {e}")


# Define regions and tags
regions_tags = {
    "eu-west-3": [
        {'Key': 'environment', 'Value': 'prod'},
        {'Key': 'team', 'Value': 'engineering'}
    ],
    "eu-central-1": [
        {'Key': 'environment', 'Value': 'dev'},
        {'Key': 'team', 'Value': 'development'}
    ]
}

# Tag instances in different regions with multiple tags
for region, tags in regions_tags.items():
    ec2_client = boto3.client('ec2', region_name=region)
    ec2_resource = boto3.resource('ec2', region_name=region)
    tag_instances(ec2_client, ec2_resource, region, tags)