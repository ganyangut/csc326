import boto.ec2

conn = boto.ec2.connect_to_region("us-east-1")

already_connected =False
reservations = conn.get_all_instances()
for reservation in reservations:
    instances = reservation.instances
    for instance in instances:        
        print "instance id: " + instance.id
        print "instance state: " + instance.state
        print "public ip address: " + repr(instance.ip_address)       
        print "root device type: " + instance.root_device_type
        print ""