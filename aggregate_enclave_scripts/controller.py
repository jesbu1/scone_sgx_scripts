#!/usr/bin/python3
import sys
import os
import requests
from flask import Flask, request, Response
import json
import uuid
import threading
import abc
import subprocess
import docker
from docker.types import Mount

client = docker.from_env()

app = Flask(__name__)
path = os.path.expanduser("~/e-mission-server/")
container_port = 1025

class DockerThread(threading.Thread):
	def __init__(self, image, query_type, container, initial_command, aggregator, mount):
		global container_port 

		threading.Thread.__init__(self)
		self.image = image
		self.query_type = query_type
		self.container = container
		self.initial_command = initial_command
		self.aggregator = aggregator
		self.mount = mount
		self.port = container_port
		container_port += 1

	def run(self):
		client.containers.run(self.image, command= self.initial_command + ' ' + self.query_type + ' ' + self.container + ' ' +  self.aggregator,
			name = self.container, remove=True, network='e-mission', ports = {str(self.port):self.port}, mounts=[self.mount], volumes={path :{'bind':'/usr/src/myapp','mode':'rw'}}, working_dir='/usr/src/myapp')

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
	#list_of_containers = ["18f729d9838a4e8ab66c3a6aac2ecdb0", "28f729d9838a4e8ab66c3a6aac2ecdb0", "38f729d9838a4e8ab66c3a6aac2ecdb0"] #open()
	list_of_containers = list(json.load(open("mock_data.json")).keys())
	query_type = str(request.data, 'utf-8')
	print(query_type)
	mount = Mount(target='/usr/src/app/conf/storage/db.conf', source= path + 'conf/storage/db.conf', type='bind')
	threads = []
	for container in list_of_containers:
		thread = DockerThread('skxu3/emission-scone3.5', query_type, container, 'bash bash_file', '35.236.79.116:80', mount)
		threads.append(thread)
		thread.start()
	for thread in threads:
		thread.join()
	return "Finished"	
if __name__ == "__main__":
	app.run(port=2000, host='0.0.0.0',debug=True)
