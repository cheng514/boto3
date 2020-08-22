'''
This script will take a snapshot of the volume with required tags, copy the snapshot to a secondary
region, and then delete the snapshot in source region.

This can be implemented for DR purposes.
'''

import boto3

source_region = "ap-southeast-2"
destination_region = "ap-southeast-1"
ec2_source = boto3.client("ec2", region_name = source_region)

paginator = ec2_source.get_paginator('describe_instances')
backup_filter = {"Name": "tag:backup", "Values": ["yes"]}
volumes = [
    volume["Ebs"]["VolumeId"]
    for pages in paginator.paginate(Filters = [backup_filter])
    for each_instance in pages["Reservations"]
    for instance in each_instance["Instances"]
    for volume in instance["BlockDeviceMappings"]
]

snapids = []
for volume in volumes:
    print(f"Taking snapshot of the volume id: {volume}")
    response = ec2_source.create_snapshot(VolumeId = volume)
    snapids.append(response["SnapshotId"])
    waiter = ec2_source.get_waiter('snapshot_completed')
    waiter.wait(SnapshotIds = snapids)

print(f"Completed snapshot for {volumes}")

ec2_dest = boto3.client("ec2", region_name = destination_region)

for snapshot in snapids:
    print(f"Copying snapshot: {snapshot} to region: {destination_region}")
    response = ec2_dest.copy_snapshot(SourceRegion = source_region, SourceSnapshotId = snapshot)
    waiter = ec2_dest.get_waiter('snapshot_completed')
    waiter.wait(SnapshotIds = [response["SnapshotId"]])
    print(f"Snapshots copied: {response['SnapshotId']}")
    ec2_source.delete_snapshot(SnapshotId = snapshot)
    print(f"Deleted snapshot in source region: {snapshot}")