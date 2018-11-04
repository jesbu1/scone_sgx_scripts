from flask import Flask, request, Response
import requests
import numpy as np
import abc
import json


class Query(abc.ABC):
	"""
	ABC is an abstract base class to define an interface for all queries
	"""
	@abc.abstractmethod
	def run_query(self, data):
		pass

	@abc.abstractmethod
	def generate_noise(self, data):
		pass

	@abc.abstractmethod
	def __repr__(self):
		pass

class Sum(Query):
	def run_query(self, data):
		self.amount_of_noise = 0
		total = 0
		for enclave in data.keys():
			try:
				value = data[enclave].text
			except:
				continue
			total += value
			self.amount_of_noise += 1
		return total

	def generate_noise(self, data):
    	sensitivity = 1
    	epsilon = 0.5
		return np.random.laplace(scale=(n * sensitivity)/epsilon)


	def __repr__(self):
		return "sum"





app = Flask(__name__)

@app.route('/start_query', methods=['POST'])
def start_query():
	"""
	1. Ask all servers stored in file/argument if they wanna respond to query
	2. Store who wants to respond to query
	3. Run query according to the query object passed in
	4. Generate noise according to the query object passed in and add to query val
	5. Return the noise
	"""
	query_mapping = {'sum' : Sum} #TODO: Fill in query mapping from string to object
	enclaves_in_query = {}
	query_object = query_mapping[request.data]

	list_of_enclaves = open('FILE FOR ALL USER ENCLAVES AND ADDRESSES')
	for enclave in list_of_enclaves:
		try:
			r = requests.post(enclave, data=str(query_object))
			r = json.loads(r)
			response = r['response']
			if response != "no" or response == "none":
				enclaves_in_query[enclave] = r['data']
		except:
			continue

	value = query_object.run_query(enclaves_in_query) + query_object.generate_noise(enclaves_in_query)
	return str(value)


@app.route('/query-example', methods=['POST'])
def query_example():
    data = int(request.data)
    print(data)
    sensitivity = 1
    epsilon = 0.5
    n = 1
    return str(np.random.laplace(scale=(n * sensitivity)/epsilon) + data)



if __name__ == "__main__":
	app.run(debug=True, port='8080')