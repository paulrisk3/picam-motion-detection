import configparser

config=configparser.ConfigParser()
config.read('picam-motion-detection.conf')
for key in config:
  #print(config[key]['url'])
  print(key)
for key in config['front_yard']:
  print(key)
