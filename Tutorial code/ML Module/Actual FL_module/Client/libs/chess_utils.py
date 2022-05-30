import chess
import chess.engine
import random
import numpy
import os

"""
Temporary code for generating Chess dataset - will be deleted when we get the data directly from the clients
- Code generates chess boards
- Chessboards are converted to 14 X 8 X 8
- Refer to https://medium.com/@nihalpuram/training-a-chess-ai-using-tensorflow-e795e1377af2 for more information
"""
FILEPATH = os.path.abspath("Completed Code/Client")

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


def stockfish(board, depth):
  filepath = FILEPATH + "\\libs\\stockfish_15_win_x64_avx2\\stockfish_15_win_x64_avx2\\stockfish_15_x64_avx2.exe"
  with chess.engine.SimpleEngine.popen_uci(filepath) as sf:
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
