import boto3
import schedule

ec2_client = boto3.client('ec2')
ec2 = boto3.resource('ec2')


# instances_create = ec2.create_instances(
#     ImageId='ami-0f403e3180720dd7e',
#     MinCount=1,
#     MaxCount=1,
#     InstanceType='t2.micro',
#     TagSpecifications=[
#         {
#             'ResourceType': 'instance',
#             'Tags': [
#                 {
#                     'Key': 'Name',
#                     'Value': 'new-ec2'
#                 }
#             ]
#         }
#     ]
# )
#
# # Wait for the instance to be running before describing it
# instances_create[0].wait_until_running()
#
# # Refresh the instance object to get the latest state
# instances_create[0].load()

# print(instances_create[0].id)
def check_instance_status():
    try:
        statuses = ec2_client.describe_instance_status(IncludeAllInstances=True)
        for status in statuses.get('InstanceStatuses', []):
            instance_id = status.get('InstanceId', 'N/A')
            ins_status = status['InstanceStatus'].get('Status', 'N/A')
            sys_status = status['SystemStatus'].get('Status', 'N/A')
            state = status['InstanceState'].get('Name', 'N/A')
            print(f"Instance {instance_id} is {state} with instance status {ins_status} and system status {sys_status}")
    except Exception as e:
        print(f"An error occurred: {e}")

schedule.every(5).seconds.do(check_instance_status)

while True:
    schedule.run_pending()


# reservations = ec2_client.describe_instances()
# for reservation in reservations['Reservations']:
#     instances = reservation['Instances']
#     for instance in instances:
#         print(f"{instance['InstanceId']} is {instance['State']['Name']}")

# # Specify the instance IDs of the EC2 instances you want to delete
# instance_ids = ['i-0f8f47aacc93498ce']
#
# # Terminate the specified EC2 instances
# response = ec2_client.terminate_instances(InstanceIds=instance_ids)
#
# print(response)
