import boto.ec2

conn = boto.ec2.connect_to_region("us-east-1")

group1 = conn.create_security_group("ping_server_group", "To ping the server")
group1.authorize("icmp", -1, -1, "0.0.0.0/0")

group2 = conn.create_security_group("ssh_group", "To allow SSH")
group2.authorize("tcp", 22, 22, "0.0.0.0/0")

group3 = conn.create_security_group("http_group", "To allow HTTP")
group3.authorize("tcp", 80, 80, "0.0.0.0/0")
