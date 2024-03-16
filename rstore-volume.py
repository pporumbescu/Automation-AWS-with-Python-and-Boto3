import boto3

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

instance_id = "i-0391fe77152d193f6"

volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'attachment.instance-id',
            'Values': [instance_id]
        }
    ]
)

if 'Volumes' in volumes:
    instance_volume = volumes['Volumes'][0]
    print(instance_volume)
else:
    print("No volumes found for the specified instance.")

