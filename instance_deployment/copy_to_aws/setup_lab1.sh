#!/bin/bash

# update list
sudo apt-get update
# install python2
sudo apt install -y python
# install pip
sudo apt install -y python-pip
# install bottle
pip install --upgrade bottle
# install oauth2client: 
pip install --upgrade oauth2client
# install beaker.middleware: 
pip install --upgrade beaker
# install Google API client: (this should also install httplib2, if not: pip install httplib2)
pip install --upgrade google-api-python-client
# install requests HTTP library.
pip install --upgrade requests
# install boto:
pip install --upgrade boto

# install sysstat and dstat for benchmark:
sudo apt-get install -y sysstat dstat

# run frontend
cd lab1_code
sudo python frontend.py