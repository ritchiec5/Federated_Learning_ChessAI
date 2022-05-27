#handle a POST request
import tensorflow
from flask import Flask, render_template, request, url_for, jsonify, send_file, send_from_directory
app = Flask(__name__)

app.config["Global_Weights"] = "C:/Users/Ritchie Chan/Desktop/3004/Federated_Learning_ChessAI/ML Module/Actual FL_module/model_weight"

@app.route('/tests/endpoint', methods=['POST', 'GET'])
def my_test_endpoint():

    if request.method == 'GET':  # Client has just initialzed and is requesting model data
        print("Sending Global Weights")
        # return send_from_directory(app.config["Global_Weights"], path="Weights", as_attachment=False))
        return send_file("C:/Users/Ritchie Chan/Desktop/3004/Federated_Learning_ChessAI/ML Module/Actual FL_module/model_weight/Weights", attachment_filename='weights')

    if request.method == 'POST':  # Client is sending model data
        input_json = request.get_json(force=True)
        print('data from client:', input_json)
        return jsonify("Recieved")


if __name__ == '__main__':
    app.run(debug=True)
