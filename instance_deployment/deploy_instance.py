import boto.ec2

conn = boto.ec2.connect_to_region("us-east-1")

already_running = False
all_terminated = True
stopped_instances = [ ]

reservations = conn.get_all_instances()
for reservation in reservations:
    instances = reservation.instances
    for instance in instances:
        if instance.state == u'running':
            already_running = True
            break
        if instance.state != u'terminated':
            all_terminated = False
        if instance.state == u'stopping' or instance.state == u'stopped':
            stopped_instances.append(instance.id)        
    if already_running:
        break

if not already_running:
    if all_terminated:
        conn.run_instances("ami-0ac019f4fcb7cb7e6", instance_type="t2.micro", key_name="waldoge_key_pair", security_groups=["csc326-group20"])
    else:
        conn.start_instances(instance_ids=stopped_instances[0], dry_run=False)   

'''
conn.get_all_instances()
conn.get_all_instances()[0].instances
conn.get_all_instances()[0].instances[0].state
conn.get_all_instances()[0].instances[0].ip_address
conn.get_all_instances()[0].instances[0].root_device_type

18.204.217.225
52.207.153.98

resp = conn.stop_instances(instance_ids="i-0bdf82d0e7b7521b4", force=False, dry_run=False)
print resp

resp = conn.terminate_instances(instance_ids=["i-0bdf82d0e7b7521b4"])
print resp

ssh -i waldoge_key_pair.pem ubuntu@18.232.160.163
scp -i waldoge_key_pair.pem -r ~/csc326 ubuntu@18.232.160.163:~/

scp -r /home/gan/csc326 ubuntu@52.207.153.98:~/

172.31.91.219
'''