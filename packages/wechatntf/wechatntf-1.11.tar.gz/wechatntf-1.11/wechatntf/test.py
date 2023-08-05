import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
# a = json.loads(config['DEFAULT']['topicIds'])
a = config["DEFAULT"]["appToken"]
print(a)
