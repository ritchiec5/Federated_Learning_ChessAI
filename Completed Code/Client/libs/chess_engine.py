from tensorflow.keras import models
import numpy
from libs.chess_ML_utils import * 


"""
get_move_from_ai:
  Gets the most optimal the AI has predicted

parameters:
  board: Chess board by chess lib
  depth: How many moves ahead to evaluate
  model: tensorflow model

return:
  str(max_move): string of the best move
"""
best_move = None
def get_move_from_ai(board, depth, model):
  global best_moves
  eval = minimax(board, depth, -numpy.inf, numpy.inf, False, model, depth)
  return str(best_move)


# def get_move_from_ai(board, depth, model):
#     best_move = None
#     alpha = numpy.inf
#     stop = False
#     for move in board.legal_moves:
#         max_eval = -numpy.inf
#         board.push(move)

#         for move1 in board.legal_moves:
#             if stop:
#                 pass
#             else:
#                 board.push(move1)
#                 eval = minimax_eval(board, model)
#                 board.pop()
#                 if(eval > alpha):
#                     stop = True
#                 max_eval = max(max_eval, eval)  # Best move for White

#         if stop == False:
#             alpha = max_eval
#             best_move = move
#         else:
#             stop = False
#         board.pop()
#     return str(best_move)

"""
minimax():
  algorithm to determine the min max of the additional depth >1
  
Parameter:
  board: Chess board by chess lib
  depth: How many moves ahead to evaluate
  alpha: determine the minimum evaluation
  beta: determine the maximum evaluation
  maximizing_player: find the best move that optimizes the player
  model: tensorflow model

return:
  min_eval: float score of the board

"""
def minimax(board, depth, alpha, beta, maximizingPlayer, model, original_depth):
  global best_move
  if depth == 0 or board.is_game_over():
    return minimax_eval(board, model)

  if maximizingPlayer:
    value = -numpy.inf
    for move in board.legal_moves:
      board.push(move)

      if depth == original_depth:
        temp_value = value
        value = max(value, minimax(board, depth - 1, alpha,
                    beta, False, model, original_depth))
        if value != temp_value:
          best_move = move
      else:
        value = max(value, minimax(board, depth - 1, alpha,
                    beta, False, model, original_depth))

      board.pop()
      if value >= beta:
        break
      alpha = max(alpha, value)
    return value

  else:
    value = numpy.inf
    for move in board.legal_moves:
      board.push(move)

      if depth == original_depth:
        temp_value = value
        value = min(value, minimax(board, depth - 1, alpha,
                  beta, True, model, original_depth))
        if value != temp_value:
          best_move = move
      else:
        value = min(value, minimax(board, depth - 1, alpha,
                  beta, True, model, original_depth))
      board.pop()
      if value <= alpha:
        break
      beta = min(beta, value)
    return value


def minimax_eval(board, model):
  board3d = split_dims(board)
  board3d = numpy.expand_dims(board3d, 0)
  return model.predict(board3d)[0][0]


"""
minimax_eval():
  predict the board evaluation score through the AI

return:
  int: model prediction score
"""
def minimax_eval(board, model):
  board3d = split_dims(board)
  board3d = numpy.expand_dims(board3d, 0)
  return model(board3d)[0][0]
