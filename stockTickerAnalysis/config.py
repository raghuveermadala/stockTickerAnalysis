import os
import configparser

# Find that config file! Wherever it is!
project_files = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser("../")) for f in fn]
# Thanks to user "John La Rooy" on stackoverflow.com for this code snippet
# https://stackoverflow.com/questions/19309667/recursive-os-listdir

for file in project_files:
    if "config.cfg" in file:
        path_to_config_file = file

config = configparser.RawConfigParser(allow_no_value=True)

try:
    config_file = open(path_to_config_file, 'r')
except IOError:
    print("Error opening config.cfg file")

config.readfp(config_file)

# Tornado port
DEFAULT = 8080
tornado_port = config.get("tornado", "port")
tornado_port = DEFAULT if tornado_port is None else tornado_port

# Memcache list of servers in hostname:port format
DEFAULT = ["127.0.0.1:11211"]
memcache_instances = []
for instance in config.items("memcache"):
    if "instance" in instance[0]:
        memcache_instances.append( str(instance[1]) )
memcache_instances = DEFAULT if memcache_instances is None else memcache_instances

# Memcache time-to-live
DEFAULT = 60
cache_ttl = int( config.get("memcache", "cache time-to-live") )
cache_ttl = DEFAULT if cache_ttl is None else cache_ttl
