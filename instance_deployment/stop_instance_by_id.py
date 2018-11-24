import boto.ec2
import sys
import time

instance_ids = sys.argv[1:]

# must provide instance ids
if not instance_ids:
    print "Please provide instance ids"
    sys.exit()

# stop instances
conn = boto.ec2.connect_to_region("us-east-1")
instances = conn.stop_instances(instance_ids=instance_ids)
if not instances:
    print "Invalid instance ids"
    sys.exit()

# check results
time.sleep(0.02)
for instance in instances:
    while instance.state == u'stopping':  
        time.sleep(0.02)
        instance.update()
    if instance.state == u'stopped':  
        print "successfully stopped:"
        print "  instance id: " + instance.id
    else:
        print "failed to stop:"
        print "  instance id: " + instance.id

