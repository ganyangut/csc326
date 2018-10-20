#!/bin/sh

#install bottle
 #$ cd <YOUR-PROJECT-DIRECTORY>
 #$ wget https://pypi.python.org/packages/source/b/bottle/bottle-0.12.7.tar.gz
 #$ tar -zxvf bottle-0.12.7.tar.gz
 #$ cd bottle-0.12.7
 #$ python setup.py install --user
 
#install module:
#oauth2client: 
pip install --upgrade oauth2client
#beaker.middleware: 
pip install beaker
#Google API client: (this should also install    httplib2, if not: pip install httplib2)
pip install --upgrade google-api-python-client

#