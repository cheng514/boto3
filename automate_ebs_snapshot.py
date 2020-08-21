'''
Take snapshot for EBS volumes according to tag name.
Used paginator to get all EC2 if more than one page.
Also included normal client code in the comment.
'''
import boto3

ec2 = boto3.client(service_name = "ec2", region_name = "ap-southeast-2")

paginator = ec2.get_paginator('describe_instances')
prod_env_filter = {"Name": "tag:env", "Values": ["prod"]}
volumes = [
    volume["Ebs"]["VolumeId"]
    for pages in paginator.paginate(Filters = [prod_env_filter])
    for each_instance in pages["Reservations"]
    for instance in each_instance["Instances"]
    for volume in instance["BlockDeviceMappings"]
]

snapids = []
for volume in volumes:
    print(f"Taking snapshot of the volume id: {volume}")
    response = ec2.create_snapshot(
        VolumeId = volume,
        TagSpecifications = [
            {
                "ResourceType": "snapshot",
                "Tags": [
                    {
                        'Key': 'delete-after',
                        'Value': '90'
                    }
                ]
            }
        ]
    )
    snapids.append(response["SnapshotId"])
waiter = ec2.get_waiter('snapshot_completed')
waiter.wait(SnapshotIds = snapids)

print(f"The snapshot for {volumes} are completed.")


# volumes = [
#     volume["Ebs"]["VolumeId"]
#     for each_insance in ec2.describe_instances(Filters = [prod_env_filter])["Reservations"]
#     for instance in each_insance["Instances"]
#     for volume in instance["BlockDeviceMappings"]
# ]

