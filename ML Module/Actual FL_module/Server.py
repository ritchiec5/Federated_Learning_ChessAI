#handle a POST request
from flask import Flask, request, jsonify, send_file
import numpy
app = Flask(__name__)

number_of_client_weights = 0
list_of_client_weights = []

def aggregration():
    pass
    # weight scaling factor
    

    # local data global data
    # 

    # scaled model weight
    # sum scaled weights
    # send back weights

def weight_scaling_factor():
    client_dataset_size = 0
    global_dataset_size = 0
    return 0.2

def scale_model_weight(client_weight, scalar):
    client_weight = numpy.array(client_weight, dtype='object')
    scaled_client_weight = client_weight * scalar
    return scaled_client_weight

def sum_scaled_weights(list_of_weights):
    global_weight = list_of_weights[0]
    for i in list_of_weights:
        if i == 0:
            pass
        else:
            global_weight = numpy.add(global_weight, list_of_weights[i+1])
    return global_weight

@app.route('/tests/endpoint', methods=['POST', 'GET'])
def my_test_endpoint():

    if request.method == 'GET':  # Client has just initialzed and is requesting model data
        print("Sending Global Weights")
        return send_file("C:/Users/Ritchie Chan/Desktop/3004/Federated_Learning_ChessAI/ML Module/Test module_Chess_AI/modelversion3.h5", attachment_filename='weights')

    if request.method == 'POST':  # Client is sending model data
        number_of_client_weights = number_of_client_weights + 1
        print("hello")
        print(request.client)
        # with open("C:/Users/Ritchie Chan/Desktop/3004/Federated_Learning_ChessAI/ML Module/Actual FL_module/client_weights/Weights{}".format(number_of_client_weights), "wb") as f:
        #     f.write(request.data)
        # f.close()
        return jsonify("Recieved")
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)
