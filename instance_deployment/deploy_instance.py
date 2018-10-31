import boto.ec2

conn = boto.ec2.connect_to_region("us-east-1")

already_running = False
all_terminated = True
stopped_instances = [ ]

# if there's already a running instance, don't do anything
reservations = conn.get_all_instances()
for reservation in reservations:
    instances = reservation.instances
    for instance in instances:
        if instance.state == u'running' or instance.state == u'pending' or instance.state == u'stopping':
            already_running = True
            break
        if instance.state != u'terminated' and instance.state != u'shutting-down':
            all_terminated = False
        if instance.state == u'stopped':
            stopped_instances.append(instance.id)        
    if already_running:
        break

if not already_running:
    if all_terminated:
        print "Start a new instance"
        conn.run_instances("ami-0ac019f4fcb7cb7e6", instance_type="t2.micro", key_name="waldoge_key_pair", security_groups=["csc326-group20"])
    else:
        print "Resume a stopped instance"
        conn.start_instances(instance_ids=stopped_instances[0], dry_run=False)   
else:
    print "There's already a running/pending/stopping instance"