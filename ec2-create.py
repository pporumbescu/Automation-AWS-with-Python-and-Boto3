import boto3
import schedule

ec2_client = boto3.client('ec2')
ec2 = boto3.resource('ec2')


instances_create = ec2.create_instances(
    ImageId='ami-0f403e3180720dd7e',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'new-ec2'
                }
            ]
        }
    ]
)

# Wait for the instance to be running before describing it
instances_create[0].wait_until_running()

# Refresh the instance object to get the latest state
instances_create[0].load()

print(instances_create[0].id)

