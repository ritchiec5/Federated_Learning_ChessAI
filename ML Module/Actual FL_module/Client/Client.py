import os 
import tensorflow
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow.keras.callbacks as callbacks
import numpy
from flask import Flask, request, jsonify
import requests
import threading
from libs.chess_utils import * 

app = Flask(__name__)

FILEPATH = os.path.abspath("ML Module/Actual FL_module/Client/")

""" 
request_global_model()
    Request global model from the server using python Request
"""
def request_global_model():
    print('Requesting Global Model from Server\n')
    res = requests.get('http://localhost:5000/server/send_global_weights',
                       json="Requesting Global model Data")
    print('Received Global Model from Server\n')
    with open(FILEPATH + "\\global_model", "wb") as f:
        f.write(res.content)
    f.close()
    print('Global Model saved')

"""
client_model_training()
    1. Train the Global Model from the Server using client dataset
    2. Clients saves the weights in a h5 file
"""
def client_model_training(dataset):
    x_train, y_train = dataset 
    x_train.transpose()
    checkpoint_filepath = '/tmp/checkpoint/'
    model_checkpointing_callback = ModelCheckpoint(
        filepath=checkpoint_filepath,
        save_best_only=True,
    )

    print("Initiated Model training/n")
    chess_model = tensorflow.keras.models.load_model(FILEPATH + "\\global_model")
    chess_model.fit(x_train, y_train,
            batch_size=2048,
            epochs=5,
            verbose=1,
            validation_split=0.1,
            callbacks=[callbacks.ReduceLROnPlateau(monitor='loss', patience=10),
                        callbacks.EarlyStopping(monitor='loss', patience=15, min_delta=1e-4), model_checkpointing_callback])
    chess_model.save_weights(FILEPATH + "\\client_weights", save_format="h5")
    print("Completed Model training/n")

"""
send_client_weights()
    Send client weights to the server 
"""
def send_client_weights():
    file = open(FILEPATH + "\\client_weights", "rb")
    params = {'client': '1', 'datasize':'100'}
    res = requests.post('http://localhost:5000/server/receive_client_weights', file, params=params)
    print('Response from server: ', res.text)

"""
receive_global_weights()
    1. receive global weights from server
    2. Save global weights in a file
"""
@app.route('/client/receive_global_weights', methods=['POST'])
def receive_global_weights():
    print("Received updated Global weights")
    if request.method == 'POST':
        filename = FILEPATH + "\\global_weights"
        with open(filename, "wb") as f:
            f.write(request.data)
        f.close()
        return jsonify("Received updated server weights")

"""
Initialize():
    Temporary function to Initialize client to train and send weights
"""
def intialize():
    request_global_model()
    dataset = create_client_dataset()
    client_model_training(dataset)
    send_client_weights()

if __name__ == '__main__':
    # Threading is utilized to allow the Flask to run without waiting for training to be completed
    intialize_thread = threading.Thread(target=intialize)  
    intialize_thread.start() 
    app.run(port=5001, debug=False)
