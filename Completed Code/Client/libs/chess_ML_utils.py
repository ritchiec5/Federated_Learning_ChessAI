"""
chess_ML_utils
  Machine learning utilities
  1. save_board(): Save the current chess position in a file
  2. create_client_dataset(): Creating Dataset based on boards position
  3. client_model_training(): Train the client based on the client dataset
"""

import chess
import chess.engine
import numpy
import os
import tensorflow
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow.keras.callbacks as callbacks

FILEPATH = os.path.abspath("Completed Code/Client")

"""
dataset_size():
  get dataset size
"""
def dataset_size():
  line_count = 0
  filepath = FILEPATH + "/client_dataset/" + "dataset.txt"
  file = open(filepath, "r")
  for line in file:
    if line != "\n":
        line_count += 1
  file.close()
  return line_count

"""
save_board():
  save the board position in a file
  Example: position saved as a string: rnbqkbnr/ppp1pppp/8/3p4/3PP3/8/PPP2PPP/RNBQKBNR b KQkq d3 0 2
"""
def save_board(chess_position):
  filepath = FILEPATH + "/client_dataset/" + "dataset.txt"
  if (os.path.exists(filepath)):
    file = open(filepath, "a")
    file.write(chess_position + "\n")

  else:
    file = open(filepath, "w")
    file.write(chess_position + "\n")
    file.close()

"""
create_client_dataset():
  Converts the string position into a numpy array for the tensorflow model to train

return:
  x_dataset: Numpy array of the chess position. 4D array [number of dataset,14,8,8]
  y_dataset: Numpy array of evaluated chess position.
"""
def create_client_dataset():
  x_dataset = []
  y_dataset = []

  # Reading client dataset and converting to array
  filepath = FILEPATH + "/client_dataset/" + "dataset.txt"
  file = open(filepath, "r")
  data = file.read()
  data = data.splitlines()

  # Loop through dataset and convert to [14,8,8] numpy array and append to a list
  print("Creating Dataset")
  for chess_position in data:
    board = chess.Board(chess_position)
    evaluation = stockfish(board, 1)
    numpy_board = split_dims(board)

    if evaluation is None:
      pass
    else:
      x_dataset.append(numpy_board)
      y_dataset.append(evaluation)

  # Convert to list of numpy array to numpy array
  x_dataset = numpy.asarray(x_dataset)
  y_dataset = numpy.asarray(y_dataset)
  y_dataset = numpy.asarray(
      y_dataset / abs(y_dataset).max() / 2 + 0.5, dtype=numpy.float32)

  return x_dataset, y_dataset


"""
client_model_training()
    1. Train the Global Model from the Server using client dataset
    2. Clients saves the weights in a h5 file
"""
def client_model_training(x_train, y_train):
    x_train.transpose()

    print("Initiated Model training\n")
    chess_model = tensorflow.keras.models.load_model(
        FILEPATH + "/model_data/global_model")
    chess_model.fit(x_train, y_train,
                    batch_size=2048,
                    epochs=5,
                    verbose=1,
                    validation_split=0.1,
                    callbacks=[callbacks.ReduceLROnPlateau(monitor='loss', patience=10),
                               callbacks.EarlyStopping(monitor='loss', patience=15, min_delta=1e-4)])
    chess_model.save_weights(
        FILEPATH + "/model_data/client_weights", save_format="h5")
    print("Completed Model training\n")


"""
stockfish():
  provides an evaluation score of the chess board position for model output
  
parameters:
  - board: chessboard position in chess lib format
  - depth: the depth determines how many moves ahead stockfish will look

return:
  score: provide a evaluation number of the position
"""

def stockfish(board, depth):
  
  filepath = FILEPATH + \
      "/libs/stockfish_15_win_x64_avx2/stockfish_15_win_x64_avx2/stockfish_15_x64_avx2.exe"
  with chess.engine.SimpleEngine.popen_uci(filepath) as sf:
    result = sf.analyse(board, chess.engine.Limit(depth=depth))
    score = result['score'].white().score()
    return score

"""
split_dims(board):

parameters:
  - board: chessboard position in chess lib format

return:
  board3d: numpy array of the board split to 3 dimension [14,8,8]

  14 - 12 different type + 2 possible boards
      12 different type of chess pieces (pawn, knight, bishop, rook, king, queen) * 2 (black, white - chess pieces) = 12
      2 possible board - 1 possible board for all black possible attack & 1 possible board for all white possible attacks
  8 by 8 - is the chess board
"""
def split_dims(board):
  # Create the board
  board3d = numpy.zeros((14, 8, 8), dtype=numpy.int8)


  # Add pieces to the matrix
  for piece in chess.PIECE_TYPES:
    for square in board.pieces(piece, chess.WHITE):
      idx = numpy.unravel_index(square, (8, 8))
      board3d[piece - 1][7 - idx[0]][idx[1]] = 1
    for square in board.pieces(piece, chess.BLACK):
      idx = numpy.unravel_index(square, (8, 8))
      board3d[piece + 5][7 - idx[0]][idx[1]] = 1

  # Add valid and attack moves for the nueral net to know what pieces are under attack
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

"""
square_to_index():
  convert square on the chess board to an index of the array
"""
# example: h3 -> 17

 
def square_to_index(square):
  letter = chess.square_name(square)
  return 8 - int(letter[1]), squares_index[letter[0]]






