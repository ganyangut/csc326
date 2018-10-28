#!/bin/bash

# read the public ip from public_ip.txt and do work
while IFS='' read -r public_ip || [[ -n "$public_ip" ]]
do
    echo "Public IP: $public_ip"
    # setup environment and run the page on aws
    ssh -i instance_deployment/waldoge_key_pair.pem ubuntu@${public_ip} 'dstat -cdnm --top-cpu --top-mem'
done < "instance_deployment/public_ip.txt"