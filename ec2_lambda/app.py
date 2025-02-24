import json
import boto3

ec2 = boto3.client('ec2')

def list_instances():
    response = ec2.describe_instances()
    instances = []
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append({
                'InstanceId': instance['InstanceId'],
                'State': instance['State']['Name'],
                'InstanceType': instance['InstanceType'],
                'PublicIpAddress': instance.get('PublicIpAddress', 'N/A'),
                'PrivateIpAddress': instance.get('PrivateIpAddress', 'N/A')
            })
    
    return instances

def filter_instances_by_state(state):
    response = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': [state]}]
    )
    instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append({
                'InstanceId': instance['InstanceId'],
                'State': instance['State']['Name'],
                'InstanceType': instance['InstanceType'],
                'PublicIpAddress': instance.get('PublicIpAddress', 'N/A'),
                'PrivateIpAddress': instance.get('PrivateIpAddress', 'N/A')
            })

    return instances

def lambda_handler(event, context):
    # Debugging logs
    print("Full Event:", json.dumps(event))

    path = event.get('rawPath', event.get('path', ''))  # Get API path
    print("Received Path:", path)  # Debugging log

    if path == "/list-instances/info":
        result = list_instances()
    elif path == "/running-instances/info":
        result = filter_instances_by_state("running")
    elif path == "/stopped-instances/info":
        result = filter_instances_by_state("stopped")
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid endpoint', 'received_path': path})
        }

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
