import configparser
import boto.ec2

config = configparser.ConfigParser()
config.read('AWS_keys.ini')
access_key_id=config['aws']['access_key_id']
secret_access_key=config['aws']['secret_access_key']
print access_key_id
print secret_access_key

conn = boto.ec2.connect_to_region("us-east-1")
'''
resp = conn.run_instances("ami-0ac019f4fcb7cb7e6", instance_type="t2.micro", key_name="waldoge_key_pair",
    security_groups=["ping_server_group", "ssh_group", "http_group"], dry_run=False)

inst = resp.instances[0]
print inst
inst.update()
print inst
'''