#!/bin/sh

# install bottle
 #$ cd <YOUR-PROJECT-DIRECTORY>
 #$ wget https://pypi.python.org/packages/source/b/bottle/bottle-0.12.7.tar.gz
 #$ tar -zxvf bottle-0.12.7.tar.gz
 #$ cd bottle-0.12.7
 #$ python setup.py install --user

# install python2
sudo apt install python
# install pip
sudo apt install python-pip
# install bottle
pip install bottle
# install oauth2client: 
pip install --upgrade oauth2client
# install beaker.middleware: 
pip install beaker
# install Google API client: (this should also install httplib2, if not: pip install httplib2)
pip install --upgrade google-api-python-client
# install boto:
pip install boto
# install awscli:
pip install awscli
# add awscli path to your $PATH:
    # import awecli in a python file
    # print awecli.__path__
    # edit ~/.bashrc 
    # add a line: export PATH=$PATH:<your_local_path>