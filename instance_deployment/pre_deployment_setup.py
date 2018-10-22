import configparser
import boto.ec2

config = configparser.ConfigParser()
config.read('AWS_keys.ini')
access_key_id=config['aws']['access_key_id']
secret_access_key=config['aws']['secret_access_key']
print access_key_id
print secret_access_key
'''
# connect to aws
conn = boto.ec2.connect_to_region("us-east-1")

# get key pair
keypair =conn.create_key_pair("waldoge_key_pair")
keypair.save("")

# create security group
group = conn.create_security_group("csc326-group20", "To ping the server, allow SSH, allow HTTP")
group.authorize("icmp", -1, -1, "0.0.0.0/0")
group.authorize("tcp", 22, 22, "0.0.0.0/0")
group.authorize("tcp", 80, 80, "0.0.0.0/0")
'''
