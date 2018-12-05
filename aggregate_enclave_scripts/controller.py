#!/usr/bin/python3
import sys
import os
import requests
from flask import Flask, request, Response, jsonify
import json
import uuid
import threading
import subprocess
import docker
from docker.types import Mount
json_data = json.load(open("mock_data.json"))
list_of_containers = list(json.load(open("mock_data.json")).keys())
client = docker.from_env()

app = Flask(__name__)
path = os.path.expanduser("~/e-mission-server/")
# container_port = 1025

class DockerThread(threading.Thread):
        def __init__(self, container, query_type, uuid, agg_ip, privacy_budget):
                threading.Thread.__init__(self)
                self.container = container
                self.query_type = query_type
                self.uuid = uuid
                self.agg_ip = agg_ip
                self.privacy_budget = privacy_budget

        def run(self):
                self.container.unpause()
                output = self.container.exec_run('bash bash_file ' + self.query_type + ' ' + self.uuid + ' ' + self.agg_ip + ' ' + self.privacy_budget)
                print(output)
                self.container.pause()

@app.route('/', methods=['GET'])
def home():
        return "hello!"

@app.route('/upload_info', methods=['POST'])
def upload():
        pass

@app.route('/remove_containers', methods=['GET'])
def remove_containers():
    for container in list_of_containers:
        container[0].remove(force=True)
    return ""
@app.route('/request_query', methods=['POST'])
def query_start():
        """
        1. Read list of enclaves from file
        2. Wake them up with docker resume
        3. Ask for query from them
        """
        request_dict = json.loads(request.data.decode('utf-8'))
        query_type = str(request_dict['query_type'])
        privacy_budget = str(request_dict['privacy_budget'])
        print(request_dict)
        threads = []
        aggregator_ip = request.environ['REMOTE_ADDR'] + ':2001'
        print("aggregator_ip: " + str(aggregator_ip))
        print("Length of list of containers: " + str(len(list_of_containers)))
        batch_size = 10
        for j in range(0, int(len(list_of_containers) / batch_size) + 1):
                for i in range(min(int(len(list_of_containers) - j * batch_size), batch_size)):
                        container = list_of_containers[j * batch_size + i]
                        thread = DockerThread(container[0], query_type, container[1], aggregator_ip, privacy_budget)
                        thread.start()
                        threads.append(thread)
                for thread in threads:
                    thread.join()
        return "Finished"       

@app.route('/start_containers', methods=['GET'])
def start():
        mount = Mount(target='/usr/src/app/conf/storage/db.conf', source= path + 'conf/storage/db.conf', type='bind')
        for i in range(len(list_of_containers)):
                container = list_of_containers[i]
                print(container)
                json_data[container]["privacy_budget"] = 10
                list_of_containers[i] = [client.containers.run('skxu3/emission-scone3.5', command = "tail -f /dev/null",
                        name = container, remove=True, devices=['/dev/isgx'], network='e-mission', mounts=[mount], volumes={path :{'bind':'/usr/src/myapp','mode':'rw'}}, working_dir='/usr/src/myapp', detach=True),
                        container]
                list_of_containers[i][0].pause()
        print(list_of_containers)
        with open("mock_data.json", "w") as jsonFile:
            json.dump(json_data, jsonFile)
        return ""

if __name__ == "__main__":
        app.run(port=2000, host='0.0.0.0',debug=True)
