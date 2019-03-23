from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import pickle
import numpy as np

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('query')

class Predict(Resource):
    def get(self):
        args = parser.parse_args()
        user_query = args['query']

        pred_text = "Hello"
        output = {'prediction': pred_text}
        return output

api.add_resource(Predict, '/')

if __name__ == '__main__':
    app.run(debug=True)