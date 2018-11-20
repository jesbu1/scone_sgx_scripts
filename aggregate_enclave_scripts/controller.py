#!/usr/bin/python3
import sys
import requests
from flask import Flask, request, Response
import json
import uuid
import threading
import abc
import numpy as np
import subprocess
import docker
from docker.types import Mount

client = docker.from_env()

app = Flask(__name__)



@app.route('/', methods=['GET'])
def home():
	return "hello!"

@app.route('/upload_info', methods=['POST'])
def upload():
	pass

@app.route('/request_query', methods=['POST'])
def query_start():
	"""
	1. Read list of enclaves from file
	2. Wake them up with docker resume
	3. Ask for query from them
	"""
	list_of_containers = ["18f729d9838a4e8ab66c3a6aac2ecdb0", "28f729d9838a4e8ab66c3a6aac2ecdb0", "38f729d9838a4e8ab66c3a6aac2ecdb0"] #open()
	#path = '/Users/Jesse/Desktop/e-mission/e-mission-server/'
	path = '/home/jsullivan27/e-mission-server/'
	ret = {}
	print(request.data)
	mount = Mount(target='/usr/src/app/conf/storage/db.conf', source= path + 'conf/storage/db.conf', type='bind')
	for container in list_of_containers:
		ret[container] = client.containers.run('skxu3/emission-scone3.5', ['python user_enclave_scripts.py ' + str(request.data) + ' ' + container],
		 name=container, remove=True, network='e-mission', ports={'8080':8080}, mounts=[mount], volumes={path :{'bind':'/usr/src/myapp','mode':'rw'}}, working_dir='/usr/src/myapp', detach=False)
		print(ret[container])
		return json.dumps(ret)
	
if __name__ == "__main__":
	app.run(port=2000)
