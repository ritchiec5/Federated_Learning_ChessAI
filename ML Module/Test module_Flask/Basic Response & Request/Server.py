#handle a POST request
import requests
from flask import Flask, render_template, request, url_for, jsonify
app = Flask(__name__)


@app.route('/tests/endpoint', methods=['POST'])
def my_test_endpoint():
    input_json = request.get_json(force=True)
    # force=True, above, is necessary if another developer
    # forgot to set the MIME type to 'application/json'
    print('data from client:', input_json)
    dictToReturn = {'answer': 42}
    return jsonify(dictToReturn)


if __name__ == '__main__':
    app.run(debug=True)
