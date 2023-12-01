#!/usr/bin/env python3
import datetime
import json
import logging
import os
import socket
import sys

import requests

# from dotenv import load_dotenv, find_dotenv
# load_dotenv()
### IF DEBUGGING IS ON THEN WE DENY ACCESS TO ALL USERS!
debug = 0

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler('/etc/openvpn/openvpn_auth.log', mode='a+', encoding='utf-8'),
    ]
)
logger = logging.getLogger()


def mylogger(message):
    timestamp = datetime.datetime.now().strftime("%a %b %e %H:%M:%S %Y us=%f")
    processname = __file__
    username = os.getenv("username")
    untrusted_ip = os.getenv("untrusted_ip")
    untrusted_port = os.getenv("untrusted_port")
    ### OPENVPN LOGGING FORMAT
    logger.info("username={0} {1}\n".format(username, message))
    # syslog.syslog(syslog.LOG_INFO, "username={0} {1}\n".format(username, message))
    return


true_socket = socket.socket


def make_bound_socket(source_ip):
    def bound_socket(*a, **k):
        sock = true_socket(*a, **k)
        sock.bind((source_ip, 0))
        return sock

    return bound_socket


if len(sys.argv) > 1:
    ip_to_use = sys.argv[1]
    socket.socket = make_bound_socket(ip_to_use)
    mylogger("Binded to " + ip_to_use)


try:
    username = os.getenv("username")
    passwd = os.getenv("password")

    if username is None:
        myerr = "username is missing"
        raise Exception(myerr)

    if passwd is None:
        myerr = "password is missing"
        raise Exception(myerr)

    ### IF DEBUGGING IS ON THEN WE DENY ACCESS TO ALL USERS!
    if debug == 1:
        mylogger(os.getresuid())
        for variable in os.environ:
            value = os.getenv(variable)
            mylogger("ENV {0}={1}".format(variable, value))
        sys.exit(1)

    ### IF DEBUGGING IS 3 WE ALLOW ALL CONNECTIONS (FOR TESTING)
    if debug == 2:
        sys.exit(0)

except Exception as e:
    mylogger(e)
    exit_val = 1
else:
    if os.path.isfile("/etc/openvpn/conf.json"):
        with open("/etc/openvpn/conf.json") as f:
        # with open("conf.json") as f:
            config = json.load(f)
    else:
        mylogger("Failed to load config file")
        sys.exit(1)

    mylogger("CLIENT AUTHORIZATION")
    data = {"username": username, "password": passwd, "secret": config["secret"]}

    for server in config["nodes"]:
        for urlKey in ["serverHostname", "serverIP"]:
            try:
                # mylogger("Using auth server: " + server['serverCity'] + " - " + server[urlKey])

                protocol = "http"
                print(data)
                if "octovpn.net" in server[urlKey]:
                    protocol = "https"

                r = requests.post(
                    protocol
                    + "://"
                    + server[urlKey]
                    + "/api/OpenVPN/Login",
                    data=data,
                    timeout=3,
                )
                r.raise_for_status()
                resp = json.loads(r.text)
                if hasattr(resp, "fail"):
                    raise Exception(resp["fail"])
                if resp["success"] == "ok":
                    mylogger("Connection successful")
                    sys.exit(0)
                else:
                    mylogger("Connection failure")
                    sys.exit(1)

            except requests.Timeout:
                # mylogger("Timed out connecting to " + server['serverCity'])
                pass
            except Exception as err:
                mylogger(err)
                pass


### IF YOU FORGET TO SET exit_val DURING SCRIPT EXECUTION
mylogger("ERROR: unexpected situation")
### DENY ACCESS
sys.exit(1)