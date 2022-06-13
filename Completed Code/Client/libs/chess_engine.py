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
# def get_move_from_ai(board, depth, model):
#   min_move = None
#   min_eval = numpy.inf

#   # Move based on the legal move and evaluate
#   # Keeps the best evaluation
#   for move in board.legal_moves:
#     board.push(move)
#     eval = minimax(board, depth - 1, -numpy.inf, numpy.inf, False, model)
#     board.pop()
#     if eval < min_eval:
#       min_eval = eval
#       min_move = move

#   return str(min_move)


def get_move_from_ai(board, depth, model):
    best_move = None
    alpha = numpy.inf
    stop = False
    for move in board.legal_moves:
        max_eval = -numpy.inf
        board.push(move)

        for move1 in board.legal_moves:
            if stop:
                pass
            else:
                board.push(move1)
                eval = minimax_eval(board, model)
                board.pop()
                if(eval > alpha):
                    stop = True
                max_eval = max(max_eval, eval)  # Best move for White

        if stop == False:
            alpha = max_eval
            best_move = move
        else:
            stop = False
        board.pop()
    return str(best_move)

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
# def minimax(board, depth, alpha, beta, maximizing_player, model):
#   if depth == 0 or board.is_game_over():
#     return minimax_eval(board, model)

#   if maximizing_player:
#     max_eval = -numpy.inf
#     for move in board.legal_moves:
#       board.push(move)
#       eval = minimax(board, depth - 1, alpha, beta, False, model)
#       board.pop()
#       max_eval = max(max_eval, eval)
#       alpha = max(alpha, eval)
#       if beta <= alpha:
#         break
#     return max_eval
#   else:
#     min_eval = numpy.inf
#     for move in board.legal_moves:
#       board.push(move)
#       eval = minimax(board, depth - 1, alpha, beta, True, model)
#       board.pop()
#       min_eval = min(min_eval, eval)
#       beta = min(beta, eval)
#       if beta <= alpha:
#         break
#     return min_eval


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
