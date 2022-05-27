#handle a POST request
import requests


# make a POST request
def request_global_model_data():
    res = requests.get('http://localhost:5000/tests/endpoint', json="Requesting Global model Data")
    print('Requesting Client model Data')
    print('response from server:', res.text)


# make a GET request
def send_client_model_data():
    res = requests.post('http://localhost:5000/tests/endpoint', json="Sending Client model Data")
    print('Sending Client model Data')
    print('response from server:', res.text)

if __name__ == '__main__':
    request_global_model_data()
    send_client_model_data()


