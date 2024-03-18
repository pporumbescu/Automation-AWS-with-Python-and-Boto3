import boto3
import schedule

ec2_client = boto3.client('ec2')
ec2 = boto3.resource('ec2')

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

