import configparser

config=configparser.ConfigParser()
config.read('picam-motion-detection.conf')
for key in config.sections():
  print(key)
  for key in config[key]:
    print(key)
