import os
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

api = Api(app)  # Require a parser to parse our POST request.
parser = reqparse.RequestParser()
parser.add_argument("dataset_req")
parser.add_argument("start_date_req")
parser.add_argument("end_date_req")
# Unpickle our model so we can use it!


class Predict(Resource):
    def post(self):
        args = parser.parse_args()  # Sklearn is VERY PICKY on how you put your values in...

        print("\nrequest is processed")
        print(args["dataset_req"])
        print(args["start_date_req"])
        print(args["end_date_req"])
        if (args["dataset_req"] == '1'):
            return {"class": 42,
                    "chart_data_1": [5, 8, 2, 4, 6, 5, 8, 2, 4, 6, 8, 9],
                    "chart_data_2": [5, 8, 2, 4, 6, 5, 7, 1, 3, 5],
                    "labels": [1, 2, 3, 4, 5, 6, 7, 8, 9]}
        elif (args["dataset_req"] == '2'):
            return {"class": 42,
                    "chart_data_1": [5, 2, 3, 5, 6, 1, 2, 3, 5, 6],
                    "chart_data_2": [5, 8, 2, 4, 6, 5, 8, 2, 4, 6],
                    "labels": [1, 2, 3, 4, 5, 6, 7, 8, 9]}
        else:
            return {"class": 500,
                    "chart_data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "chart_data_2": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "labels": [1, 2, 3, 4, 5, 6, 7, 8, 9]}


api.add_resource(Predict, "/predict")

if __name__ == "__main__":
    print("Starting server.")
    app.run(debug=True)
