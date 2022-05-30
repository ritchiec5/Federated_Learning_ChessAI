from time import sleep
from flask import Flask, jsonify, render_template, request
import threading 
from chess_engine import *
from libs.chess_utils import *
import tensorflow
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow.keras.callbacks as callbacks
import requests

app = Flask(__name__)
FILEPATH = os.path.abspath("Completed Code/Client")
model = None  # Global variable to store tensorflow model


""" 
request_global_model()
    Request global model from the server using python Request
"""
def request_global_model():
    global model
    
    print('Requesting Global Model from Server\n')
    res = requests.get('http://localhost:5000/server/send_global_weights',
                       json="Requesting Global model Data")
    print('Received Global Model from Server\n')
    with open(FILEPATH + "\\global_model", "wb") as f:
        f.write(res.content)
    f.close()
    print('Global Model saved')

    # Initialize tensorflow model
    model = tensorflow.keras.models.load_model(FILEPATH + "\\global_model")
    

"""
client_model_training()
    1. Train the Global Model from the Server using client dataset
    2. Clients saves the weights in a h5 file
"""
def client_model_training():
    x_train, y_train = create_client_dataset()
    x_train.transpose()
    checkpoint_filepath = '/tmp/checkpoint/'
    model_checkpointing_callback = ModelCheckpoint(
        filepath=checkpoint_filepath,
        save_best_only=True,
    )

    print("Initiated Model training\n")
    chess_model = tensorflow.keras.models.load_model(
        FILEPATH + "\\global_model")
    chess_model.fit(x_train, y_train,
                    batch_size=2048,
                    epochs=5,
                    verbose=1,
                    validation_split=0.1,
                    callbacks=[callbacks.ReduceLROnPlateau(monitor='loss', patience=10),
                               callbacks.EarlyStopping(monitor='loss', patience=15, min_delta=1e-4), model_checkpointing_callback])
    chess_model.save_weights(FILEPATH + "\\client_weights", save_format="h5")
    print("Completed Model training/n")
    send_client_weights()

"""
send_client_weights()
    Send client weights to the server 
"""
def send_client_weights():
    file = open(FILEPATH + "\\client_weights", "rb")
    params = {'client': '1', 'datasize': '100'}
    res = requests.post(
        'http://localhost:5000/server/receive_client_weights', file, params=params)
    print('Response from server: ', res.text)


@app.route('/')
def index():
    request_model_thread = threading.Thread(target=request_global_model)
    request_model_thread.start()
    return render_template("index.html")


@app.route('/move/<int:depth>/<path:fen>/')
def get_move(depth, fen):
    global model

    while (model is None):
        print("Model has not been initialized")
        sleep(5)
    
    # Save the chessboard position for model training
    save_board(fen)

    # Calculate best chess move with the tensorflow model
    print("Calculating...")
    board  = chess.Board(fen)
    depth = 1 # Currently depth of more than 1, exponentially increase the computing time. Will have to dig deeper into minmax algo.
    move = engine(board, depth, model)
    print("Move found!", move)
    return move


@app.route('/gameover/', methods=['POST'])
def game_over():
    model_training_thread = threading.Thread(target=client_model_training)
    model_training_thread.start()
    return "Gameover"

"""
receive_global_weights()
    1. receive global weights from server
    2. Save global weights in a file
"""
@app.route('/client/receive_global_weights', methods=['POST'])
def receive_global_weights():
    print("Received updated Global weights")
    if request.method == 'POST':
        filename = FILEPATH + "\\updated_global_weights"
        with open(filename, "wb") as f:
            f.write(request.data)
        f.close()
        return jsonify("Received updated server weights")

if __name__ == '__main__':
    app.run(port=5001, debug=False)
