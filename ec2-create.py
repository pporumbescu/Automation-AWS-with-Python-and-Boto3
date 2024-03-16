import boto3
from botocore.exceptions import ClientError
import os

# Initialize the EC2 client and resource from Boto3
ec2_client = boto3.client('ec2')
ec2 = boto3.resource('ec2')

def create_ec2_instance(image_id, instance_type, instance_name):
    """
    Create an EC2 instance with specified image ID, instance type, and name.
    """
    try:
        instances = ec2.create_instances(
            ImageId=image_id,
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': instance_name
                        }
                    ]
                }
            ]
        )
        instance = instances[0]
        print(f"Creating instance {instance.id}...")
        instance.wait_until_running()
        print(f"Instance {instance.id} is now running.")
        return instance
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    # Use environment variables or replace with your own values
    image_id = os.getenv('AWS_EC2_AMI_ID', 'ami-0f403e3180720dd7e')
    instance_type = os.getenv('AWS_EC2_INSTANCE_TYPE', 't2.micro')
    instance_name = 'new-ec2'  # Consider generating or passing this dynamically for multiple instances

    # Create the EC2 instance
    instance = create_ec2_instance(image_id, instance_type, instance_name)
    if instance:
        print(f"Successfully created and started instance {instance.id} with name '{instance_name}'.")

