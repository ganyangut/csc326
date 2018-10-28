import boto.ec2
import time

conn = boto.ec2.connect_to_region("us-east-1")

already_connected =False
reservations = conn.get_all_instances()
for reservation in reservations:
    instances = reservation.instances
    for instance in instances:
        while instance.state == u'pending':  
            time.sleep(0.02)
            instance.update()
        if instance.state == u'running':  
            print "running:"
            print "  instance id: " + instance.id
            print "  public ip address: " + instance.ip_address       
            print "  root device type: " + instance.root_device_type    
            with open("public_ip.txt", 'w') as write_file:
                write_file.write(instance.ip_address)
            already_connected = True
            break        
    if already_connected:
        break
else:
    print "No running instance."     