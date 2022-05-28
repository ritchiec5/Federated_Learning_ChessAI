#handle a POST request
import threading
from flask import Flask, request, jsonify, send_file
import requests
import numpy
import tensorflow
app = Flask(__name__)

number_of_client_weights = 0
list_of_client_weights = []

global_dataset_size = 0
client_dataset_size_list = []


def aggregration():
    global list_of_client_weights
    model = tensorflow.keras.models.load_model(
        "C:/Users/Ritchie Chan/Desktop/3004/Federated_Learning_ChessAI/ML Module/Actual FL_module/global_model/global_model")
    model.load_weights("C:/Users/Ritchie Chan/Desktop/3004/Federated_Learning_ChessAI/ML Module/Actual FL_module/client_weights/Weights1")
    
    weight_scaling_factor_list = weight_scaling_factor()
    scaled_client_weights = scale_model_weight(weight_scaling_factor_list, model)
    sum_scaled_weights(scaled_client_weights, model)
    send_client_updated_weights()


def weight_scaling_factor():
    global global_dataset_size
    print(client_dataset_size_list)
    
    weight_scaling_factor_list = [
        client_datasize / global_dataset_size for client_datasize in client_dataset_size_list]
    print(weight_scaling_factor_list)
    return weight_scaling_factor_list


def scale_model_weight(weight_scaling_factor_list, model):
    scaled_client_weights = []
    print(list_of_client_weights)
    for i, scaling_factor in enumerate(weight_scaling_factor_list):
        print(i)
        filepath = list_of_client_weights[int(i)]
        model.load_weights(filepath)
        client_weight = model.get_weights()
        client_weight = numpy.array(client_weight, dtype='object')
        scaled_client_weights.append(client_weight * scaling_factor)
    return scaled_client_weights

def sum_scaled_weights(scaled_client_weights, model):
    global_weight = scaled_client_weights[0]
    # print(scaled_client_weights[0])
    # print(scaled_client_weights)
    for client_weight in scaled_client_weights[1:]:
        global_weight = numpy.add(global_weight, client_weight)
    model.set_weights(global_weight)
    model.save_weights(
        "C:/Users/Ritchie Chan/Desktop/3004/Federated_Learning_ChessAI/ML Module/Actual FL_module/client_weights/server_weights", save_format="h5")


def send_client_updated_weights():
    file = open("C:/Users/Ritchie Chan/Desktop/3004/Federated_Learning_ChessAI/ML Module/Actual FL_module/client_weights/Weights", "rb")
    res = requests.post(
        'http://localhost:5001/tests/endpoint1', file)

@app.route('/tests/endpoint', methods=['POST', 'GET'])
def my_test_endpoint():
    global number_of_client_weights
    global global_dataset_size
    global filename
    global client_dataset_size_list

    if request.method == 'GET':  # Client has just initialzed and is requesting model data
        print("Sending Global Weights")
        return send_file("C:/Users/Ritchie Chan/Desktop/3004/Federated_Learning_ChessAI/ML Module/Test module_Chess_AI/modelversion3.h5", attachment_filename='weights')

    if request.method == 'POST':  # Client is sending model data

        client_id = request.args.get("client") 
        client_dataset_size = request.args.get("datasize")

        filename = "C:/Users/Ritchie Chan/Desktop/3004/Federated_Learning_ChessAI/ML Module/Actual FL_module/client_weights/Weights{}".format(
            client_id)
        with open(filename, "wb") as f:
            f.write(request.data)
        f.close()
        number_of_client_weights = number_of_client_weights + 1
        client_dataset_size_list.append(int(client_dataset_size))
        global_dataset_size = global_dataset_size + int(client_dataset_size)
        list_of_client_weights.append(filename)

        aggregration_thread = threading.Thread(target=aggregration)
        aggregration_thread.start()
        return jsonify("Recieved")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
