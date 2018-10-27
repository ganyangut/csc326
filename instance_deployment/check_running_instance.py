import boto.ec2

conn = boto.ec2.connect_to_region("us-east-1")

already_connected =False
reservations = conn.get_all_instances()
for reservation in reservations:
    instances = reservation.instances
    for instance in instances:
        if instance.state == u'running':  
            print "instance id: " + instance.id
            print "public ip address: " + instance.ip_address       
            print "root device type: " + instance.root_device_type    
            already_connected = True
            break        
    if already_connected:
        break
else:
    print "No running instance."     