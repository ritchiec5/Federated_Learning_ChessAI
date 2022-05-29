import chess
import chess.engine
import random
import numpy
import os

FILEPATH = os.path.abspath("Completed Code/FlaskChess")

def create_client_dataset():
    x_dataset = []
    y_dataset = []

    print("Creating Dataset")
    for i in range(10):
        print("Dataset ", i, ": created")
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
    y_dataset = numpy.asarray(
        y_dataset / abs(y_dataset).max() / 2 + 0.5, dtype=numpy.float32)
    print(y_dataset)

    return x_dataset, y_dataset

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
          r'C:\Users\Ritchie Chan\Desktop\3004\Federated_Learning_ChessAI\ML Module\Test module_Chess_AI\stockfish_15_win_x64_avx2\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe') as sf:
    result = sf.analyse(board, chess.engine.Limit(depth=depth))
    score = result['score'].white().score()
    return score

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


def save_board(chess_position):

  filepath = FILEPATH + "/client_dataset/" + "dataset.txt"

  if (os.path.exists(filepath)):
    file = open(filepath, "a")
    file.write(chess_position + "\n")

  else: 
    file = open(filepath, "w")
    file.write(chess_position + "\n")
    file.close()

  # file = open(filepath,"r")
  # data = file.read()
  # data = data.splitlines()
  # print(data)

# for x in range(6):
#   save_board("r1b1kb1r/ppp1pppp/2nq1n2/1K1p4/8/8/PPPP1PPP/RNBQ1BNR b kq - 5 7")
  
  # dataset_number = 0
  # board = chess.Board(chess_position)
  # stockfish(board)
  # numpy_board = split_dims(board)

  # os.makedirs(FILEPATH + "/client_dataset/", exist_ok=True)
  # filepath = FILEPATH + "/client_dataset/" + "{}.npy".format(dataset_number)
  # while (os.path.exists(filepath)):
  #   dataset_number = dataset_number + 1
  #   filepath = FILEPATH + "/client_dataset/" + "{}.npy".format(dataset_number)
  # numpy.save(filepath, numpy_board)


