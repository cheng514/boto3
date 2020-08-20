'''
Auto start VMs with the tag of env:test
'''

import boto3

def lambda_handler(event, context):
    ec2 = boto3.client("ec2", region_name = "ap-southeast-2")
    
    test_env_filter = {"Name": "tag:env", "Values": ["test"]}
    for items in ec2.describe_instances(Filters = [test_env_filter])["Reservations"]:
        for item in items["Instances"]:
            ec2.start_instances(InstanceIds = [item["InstanceId"]])