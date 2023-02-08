import numpy as np
import configparser

cf = configparser.ConfigParser()
cf.read("config.ini")

secs = cf.sections()
print(secs)

options = cf.options("Account")
print(options)

items = cf.items("Account")
print(items)

host = cf.getint("Account", "email")
print(host)
