from flask import Flask, render_template, request, url_for, jsonify
app = Flask(__name__)


@app.route('/tests/endpoint', methods=['POST', 'GET'])
def my_test_endpoint():

    if request.method == 'GET':  # Client has just initialzed and is requesting model data
        return("Send Global Model Weights")

    if request.method == 'POST': # Client is sending model data
        input_json = request.get_json(force=True) 
        print ('data from client:', input_json)
        return jsonify("Received Client Model Weights ")


if __name__ == '__main__':
    app.run(debug=True)
