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

def build_model(conv_size, conv_depth):
  board3d = layers.Input(shape=(14, 8, 8))

  # adding the convolutional layers
  x = board3d
  for _ in range(conv_depth):
    x = layers.Conv2D(filters=conv_size, kernel_size=3,
                      padding='same', activation='relu')(x)
  x = layers.Flatten()(x)
  x = layers.Dense(64, 'relu')(x)
  x = layers.Dense(1, 'sigmoid')(x)

  return models.Model(inputs=board3d, outputs=x)

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
    model = build_model(32, 4)
    x_train, y_train = create_client_dataset()

    x_train.transpose()
    print(x_train.shape)
    print(y_train.shape)
    model.compile(optimizer=optimizers.Adam(5e-4), loss='mean_squared_error')
    model.summary()
    checkpoint_filepath = '/tmp/checkpoint/'
    model_checkpointing_callback = ModelCheckpoint(
        filepath=checkpoint_filepath,
        save_best_only=True,
    )
    model.load_weights("C:/Users/Ritchie Chan/Desktop/3004/Federated_Learning_ChessAI/ML Module/Test module_Chess_AI/test_weight/global_weight")
    model.fit(x_train, y_train,
            batch_size=2048,
            epochs=20,
            verbose=1,
            validation_split=0.1,
            callbacks=[callbacks.ReduceLROnPlateau(monitor='loss', patience=10),
                        callbacks.EarlyStopping(monitor='loss', patience=15, min_delta=1e-4), model_checkpointing_callback])


# make a POST request
def request_global_model_data():
    res = requests.get('http://localhost:5000/tests/endpoint',
                       json="Requesting Global model Data")
    print('Requesting Client model Data')
    print(res.content)
    print('response from server:', res.content)
    with open("global_weight", "wb") as f:
        f.write(res.content)
    f.close()


# make a GET request
def send_client_model_data():
    res = requests.post('http://localhost:5000/tests/endpoint',
                        json="Sending Client model Data")
    # print('Sending Client model Data')
    print('response from server:', res.text)


if __name__ == '__main__':
    # get_client_dataset()
    weights = request_global_model_data()
    print(weights)
    client_model_training()
    send_client_model_data()

