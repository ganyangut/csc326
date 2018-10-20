import boto.ec2

conn = boto.ec2.connect_to_region("us-east-1")

keypair =conn.create_key_pair("waldoge_key_pair")
keypair.save("")
