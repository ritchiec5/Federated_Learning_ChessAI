from flask import Flask, render_template
import threading 
from chess_engine import *
from libs.chess_utils import *
import tensorflow

model = tensorflow.keras.models.load_model('C:/Users/Ritchie Chan/Desktop/3004/Federated_Learning_ChessAI/Completed Code/FlaskChess/global_model.h5')

app = Flask(__name__)
FILEPATH = os.path.abspath("Completed Code/FlaskChess")

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/move/<int:depth>/<path:fen>/')
def get_move(depth, fen):
    global model
    print("Calculating...")

    # Save the chessboard position for model training
    save_board_thread = threading.Thread(target=save_board, args=(fen,))
    save_board_thread.start()

    board  = chess.Board(fen)
    move = engine(board, 1, model)
    print("Move found!", move)
    return move


@app.route('/test/<string:tester>')
def test_get(tester):
    return tester


if __name__ == '__main__':
    app.run(debug=True)
