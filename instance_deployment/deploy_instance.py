import boto.ec2
import sys
import time

stopped_instances = [ ]
conn = boto.ec2.connect_to_region("us-east-1")
instances = conn.get_only_instances()

# check current instances
for instance in instances:    
    # wait for pending/stopping/shutting-down instances
    while instance.state == u'pending' or instance.state == u'stopping' or instance.state == u'shutting-down':  
        time.sleep(0.02)
        instance.update()
    # if there's already a running instance, don't do anything
    if instance.state == u'running':
        print "There's already a running instance"
        print "  instance id: " + instance.id
        print "  public ip address: " + instance.ip_address       
        print "  root device type: " + instance.root_device_type    
        with open("public_ip.txt", 'w') as write_file:
            write_file.write(instance.ip_address)     
        sys.exit()   
    # prepare to resume stopped instances
    if instance.state == u'stopped':
        stopped_instances.append(instance.id)        

# deploy a instance
if stopped_instances:
    print "Resume a stopped instance"
    conn.start_instances(instance_ids=stopped_instances[0], dry_run=False)   
else:
    print "Start a new instance"
    conn.run_instances("ami-0ac019f4fcb7cb7e6", instance_type="t2.micro", key_name="waldoge_key_pair", security_groups=["csc326-group20"])   

# check deployment result
time.sleep(0.02)
instances = conn.get_only_instances()
for instance in instances:
    while instance.state == u'pending':  
        time.sleep(0.02)
        instance.update()
    if instance.state == u'running':  
        print "deployment success:"
        print "  instance id: " + instance.id
        print "  public ip address: " + instance.ip_address       
        print "  root device type: " + instance.root_device_type    
        with open("public_ip.txt", 'w') as write_file:
            write_file.write(instance.ip_address)
        break        
else:
    print "deployment failure"