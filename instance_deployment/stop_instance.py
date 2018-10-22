import boto.ec2

conn = boto.ec2.connect_to_region("us-east-1")

reservations = conn.get_all_instances()
for reservation in reservations:
    reservation.stop_all()    

#conn.stop_instances(instance_ids="i-0491cd230b9e1e447", force=False, dry_run=False)