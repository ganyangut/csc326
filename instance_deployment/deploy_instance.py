import configparser


config = configparser.ConfigParser()
config.read('AWS_keys.ini')
access_key_id=config['aws']['access_key_id']
secret_access_key=config['aws']['secret_access_key']
print access_key_id
print secret_access_key