import boto3
from botocore.exceptions import ClientError

# Specify the instance IDs and their corresponding regions
instances = {
    'i-09ce071be381753ca': 'eu-central-1',
    'i-0ecaa18f89a64a820': 'us-east-1'
}

for instance_id, region in instances.items():
    ec2_client = boto3.client('ec2', region_name=region)

    try:
        # Attempt to terminate the specified EC2 instance in the current region
        response = ec2_client.terminate_instances(InstanceIds=[instance_id])

        # Print the termination status of the instance
        for instance in response['TerminatingInstances']:
            print(f"Instance {instance['InstanceId']} in {region} - Current State: {instance['CurrentState']['Name']}")

    except ClientError as error:
        print(f"Failed to terminate instance {instance_id} in {region}. Error: {error}")
