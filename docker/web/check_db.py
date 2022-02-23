import os
import re
import socket
import time

import environ

# Default
service_name = "Postgres"
ip = "db"
port = 5432

env = environ.Env()
env_path = os.path.join(os.getcwd(), "src/app/local.env")

if os.path.exists(env_path):
    environ.Env.read_env(str(env_path))
    DATABASE_URL = env.str("DATABASE_URL", None)

    # DATABASE_URL=postgres://user:password@domain.amazonaws.com:port/name
    if DATABASE_URL:
        service_name = re.findall(r".+(?=:\/)", DATABASE_URL)[0]
        ip = re.findall(r"(?<=@)[^:]*", DATABASE_URL)[0]
        port = int(re.findall(r"(?<=:)[0-9]{4}", DATABASE_URL)[0])

# Infinite loop
while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((ip, port))
    if result == 0:
        print("{0} port is open! Bye!".format(service_name))
        break
    else:
        print("{0} port is not open! I'll check it soon!".format(service_name))
        time.sleep(10)
