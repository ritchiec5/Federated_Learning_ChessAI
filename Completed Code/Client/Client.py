from time import sleep
from flask import Flask, jsonify, render_template, request
import threading 
from libs.chess_engine import *
from libs.chess_ML_utils import *
import tensorflow
import sys

import requests

app = Flask(__name__)
model = None  # Global variable to store tensorflow model

FLASK_PORT = str(sys.argv[1])
STOCKFISH_PORT = str(sys.argv[2])

# FILEPATH = "./Completed Code/Client"
FILEPATH = ""
SERVERIP = "http://192.168.1.154:5000/"


""" 
request_global_model()
    Request global model from the server using python Request
"""
def request_global_model():
    global model
    print('Requesting Global Model from Server\n')
    res = requests.get(SERVERIP + 'server/send_global_weights',
                       json="Requesting Global model Data")
    print('Received Global Model from Server\n')
    with open(FILEPATH + "/model_data/global_model.h5", "wb") as f:
        f.write(res.content)
    f.close()
    print('Global Model saved')

    # Initialize tensorflow model
    try:
        model = tensorflow.keras.models.load_model(FILEPATH + "/model_data/global_model.h5")
    except:
        print("File corrupted, Requesting Global model")
        request_global_model()
        
"""
send_client_weights()
    Send client weights to the server 
"""
def send_client_weights():
    file = open(FILEPATH + "/model_data/client_weights", "rb")
    datasize = dataset_size()
    params = {'datasize': str(datasize), 'port_number': port_number}
    
    res = requests.post(
        SERVERIP + '/server/receive_client_weights', file, params=params)
    print('Response from server: ', res.text)

"""
training_thread():
    1. Create client dataset based on chess position
    2. Train the client model and save into model_data/client_weights
    2. Send client weights to server
"""
def training_thread():
    x_dataset, y_dataset = create_client_dataset(STOCKFISH_PORT)
    client_model_training(x_dataset, y_dataset)
    send_client_weights()

"""
index():
    1. initialize the global model by sending request
    2. render the chess board to play on web interface

return:
    - render the chess page to play
"""
@app.route('/')
def index():
    global port_number
    port_number = request.host
    request_model_thread = threading.Thread(target=request_global_model)
    request_model_thread.start()
    return render_template("index.html")


"""
get_move(depth, fen):
    1. save chess board position for model training
    2. calculate best chess move using the chess AI 

Parameters:
    - depth: calculate depth for minmax algorithm
    - fen: particular chess position

return:
    move: returns a string of the best move
"""
@app.route('/move/<int:depth>/<path:fen>/')
def get_move(depth, fen):
    global model

    while (model is None):
        print("Model has not been initialized")
        sleep(5)
        request_global_model()
    
    # Save the chessboard position for model training
    save_board(fen)

    # Calculate best chess move with the tensorflow model
    print("Calculating...")
    board  = chess.Board(fen)
    # Currently depth of more than 2, exponentially increase the computing time.
    move = get_move_from_ai(board, depth, model)
    print("Move found!", move)
    return move


"""
game_over(depth, fen):
    1. initiate the model training when the game is over

return:
    response: string
"""
@app.route('/gameover/', methods=['POST'])
def game_over():
    print("game_over")
    model_training_thread = threading.Thread(target=training_thread)
    model_training_thread.start()
    return "Gameover"


"""
receive_global_weights()
    1. receive global weights from server
    2. Save global weights in a file

return:
    response: json string 
"""
@app.route('/client/receive_global_weights', methods=['POST'])
def receive_global_weights():
    print("Received updated Global weights")
    if request.method == 'POST':
        filename = FILEPATH + "/model_data/updated_global_weights"
        with open(filename, "wb") as f:
            f.write(request.data)
        f.close()
        return jsonify("Received updated server weights")

if __name__ == '__main__':
    app.run(port=FLASK_PORT, debug=False, host='0.0.0.0')
