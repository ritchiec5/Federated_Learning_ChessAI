import threading
import chess
import random
import chess.engine
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow.keras.callbacks as callbacks
import requests
import tensorflow.keras.models as models
import tensorflow.keras.layers as layers
import tensorflow.keras.utils as utils
import tensorflow.keras.optimizers as optimizers
import numpy
from flask import Flask, request, jsonify, send_file
import tensorflow
app = Flask(__name__)


squares_index = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7
}

# example: h3 -> 17
def square_to_index(square):
  letter = chess.square_name(square)
  return 8 - int(letter[1]), squares_index[letter[0]]

def split_dims(board):
  # this is the 3d matrix
  board3d = numpy.zeros((14, 8, 8), dtype=numpy.int8)

  # here we add the pieces's view on the matrix
  for piece in chess.PIECE_TYPES:
    for square in board.pieces(piece, chess.WHITE):
      idx = numpy.unravel_index(square, (8, 8))
      board3d[piece - 1][7 - idx[0]][idx[1]] = 1
    for square in board.pieces(piece, chess.BLACK):
      idx = numpy.unravel_index(square, (8, 8))
      board3d[piece + 5][7 - idx[0]][idx[1]] = 1

  # add attacks and valid moves too
  # so the network knows what is being attacked
  aux = board.turn
  board.turn = chess.WHITE
  for move in board.legal_moves:
      i, j = square_to_index(move.to_square)
      board3d[12][i][j] = 1
  board.turn = chess.BLACK
  for move in board.legal_moves:
      i, j = square_to_index(move.to_square)
      board3d[13][i][j] = 1
  board.turn = aux

  return board3d

# this function will create our x (board)
def random_board(max_depth=200):
  board = chess.Board()
  depth = random.randrange(0, max_depth)

  for _ in range(depth):
    all_moves = list(board.legal_moves)
    random_move = random.choice(all_moves)
    board.push(random_move)
    if board.is_game_over():
      break

  return board

# this function will create our f(x) (score)
def stockfish(board, depth):
  with chess.engine.SimpleEngine.popen_uci(
          r'C:/Users/Ritchie Chan/Desktop/3004/Federated_Learning_ChessAI/ML Module/Test module_Chess_AI/stockfish_15_win_x64_avx2/stockfish_15_win_x64_avx2/stockfish_15_x64_avx2.exe') as sf:
    result = sf.analyse(board, chess.engine.Limit(depth=depth))
    score = result['score'].white().score()
    return score

""" This function will be updated to get dataset from the games played """
def create_client_dataset():
    x_dataset = []
    y_dataset = []

    print("Creating Dataset")
    for i in range(10):
        print("Dataset ",i, ": created")
        board = random_board()
        eval = stockfish(board, 1)
        print("Stockfish: ", eval)
        data_board = split_dims(board)
        
        if eval is None:
            pass
        else:
            x_dataset.append(data_board)
            y_dataset.append(eval)
    
    x_dataset = numpy.asarray(x_dataset)
    y_dataset = numpy.asarray(y_dataset)
    y_dataset = numpy.asarray(y_dataset / abs(y_dataset).max() / 2 + 0.5, dtype=numpy.float32)
    print(y_dataset)

    return x_dataset, y_dataset


def client_model_training():
    # model = build_model(32, 4)
    x_train, y_train = create_client_dataset()
    x_train.transpose()
    checkpoint_filepath = '/tmp/checkpoint/'
    model_checkpointing_callback = ModelCheckpoint(
        filepath=checkpoint_filepath,
        save_best_only=True,
    )
    new_model = tensorflow.keras.models.load_model("C:/Users/Ritchie Chan/Desktop/3004/Federated_Learning_ChessAI/ML Module/Actual FL_module/global_model/global_model")
    new_model.fit(x_train, y_train,
            batch_size=2048,
            epochs=20,
            verbose=1,
            validation_split=0.1,
            callbacks=[callbacks.ReduceLROnPlateau(monitor='loss', patience=10),
                        callbacks.EarlyStopping(monitor='loss', patience=15, min_delta=1e-4), model_checkpointing_callback])
    new_model.save_weights("C:/Users/Ritchie Chan/Desktop/3004/Federated_Learning_ChessAI/ML Module/Actual FL_module/client_weights/client_weights", save_format="h5")

# make a GET request
def request_global_model_data():
    res = requests.get('http://localhost:5000/tests/endpoint',
                       json="Requesting Global model Data")
    print('Requesting Client model Data')
    print(res.content)
    print('response from server:', res.content)
    with open("C:/Users/Ritchie Chan/Desktop/3004/Federated_Learning_ChessAI/ML Module/Actual FL_module/global_model/global_model", "wb") as f:
        f.write(res.content)
    f.close()


# make a POST request
def send_client_model_data():
    file = open("C:/Users/Ritchie Chan/Desktop/3004/Federated_Learning_ChessAI/ML Module/Actual FL_module/client_weights/Weights", "rb")
    params = {'client': '1', 'datasize':'100'}
    res = requests.post('http://localhost:5000/tests/endpoint', file, params=params)
    print('response from server:', res.text)


@app.route('/tests/endpoint1', methods=['POST'])
def my_test_endpoint():

    print("Recieved Global weights")
    if request.method == 'POST':  # Client is sending model data

        filename = "C:/Users/Ritchie Chan/Desktop/3004/Federated_Learning_ChessAI/ML Module/Actual FL_module/client_weights/global_weights"
        with open(filename, "wb") as f:
            f.write(request.data)
        f.close()
        # To implement concurrency
        return jsonify("Recieved")


def intialize():
    request_global_model_data()
    client_model_training()
    send_client_model_data()


if __name__ == '__main__':
    intialize_thread = threading.Thread(target=intialize)
    intialize_thread.start()
    app.run(port=5001, debug=False)

