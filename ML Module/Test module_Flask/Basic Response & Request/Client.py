#make a POST request
import requests
dictToSend = {'question': 'what is the answer?'}
res = requests.post('http://localhost:5000/tests/endpoint', json=dictToSend)
print ('response from server:', res.text)
dictFromServer = res.json()
