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

app = Flask(__name__)




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
	list_of_containers = ['kate', 'jesse', 'jack'] #open()
	path = '/Users/Jesse/Desktop/e-mission/e-mission-server/'
	ret = {}
	for container in list_of_containers:

		ret[container] = ret.append(client.containers.run('skxu3/emission-scone3.5', 'pip install flask', name='kate', network='e-mission', ports={'8080':8080}, mounts=[mount], volumes={path :{'bind':'/usr/src/myapp','mode':'rw'}}, working_dir='/usr/src/myapp', detach=False))
	return json.dumps(ret)
