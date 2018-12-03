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
list_of_containers = []
client = docker.from_env()

app = Flask(__name__)
path = os.path.expanduser("~/e-mission-server/")
# container_port = 1025

class DockerThread(threading.Thread):
	def __init__(self, container, query_type, uuid, agg_ip):
		threading.Thread.__init__(self)
		self.container = container
		self.query_type = query_type
		self.uuid = uuid
		self.agg_ip = agg_ip

	def run(self):
		self.container.unpause()
		self.container.run_exec(self.query_type + ' ' + self.uuid + ' ' + self.agg_ip)
		self.container.pause()

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
	query_type = str(request.data, 'utf-8')
	print(query_type)
	threads = []
	for j in range(0, int(len(list_of_containers) / 5) + 1):
		for i in range(min(int(len(list_of_containers) - j * 5), 5)):
			container = list_of_containers[j * 5 + i]
			thread = DockerThread(container[0], query_type, container[1], '35.236.79.116:80')
			thread.start()
		for thread in threads:
			thread.join()
	return "Finished"	

@app.route('/start_containers', methods['POST'])
def start():
	list_of_containers = list(json.load(open("mock_data.json")).keys())
	mount = Mount(target='/usr/src/app/conf/storage/db.conf', source= path + 'conf/storage/db.conf', type='bind')
	for i in range(len(list_of_containers)):
		container = list_of_containers[i]
		print(container)
		list_of_containers[i] = [client.containers.run('skxu3/emission-scone3.5', command = "bash bash_file",
			name = container, remove=True, network='e-mission', mounts=[mount], volumes={path :{'bind':'/usr/src/myapp','mode':'rw'}}, working_dir='/usr/src/myapp', detach=True),
			container]
		list_of_containers[i][0].pause()
	print(list_of_containers)

if __name__ == "__main__":
	app.run(port=2000, host='0.0.0.0',debug=True)
