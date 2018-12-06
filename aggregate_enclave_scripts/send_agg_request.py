import requests
import json

r1 = requests.post("http://128.32.37.205:2001/start_query", data=json.dumps({'query_type':'sum', 'privacy_budget':6}))
r2 = requests.post("http://128.32.37.205:2001/start_query", data=json.dumps({'query_type':'sum', 'privacy_budget':6}))