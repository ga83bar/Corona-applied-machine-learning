import os
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

api = Api(app)# Require a parser to parse our POST request.
parser = reqparse.RequestParser()
parser.add_argument("dataset_req")
# Unpickle our model so we can use it!

class Predict(Resource):
  def post(self):
    args = parser.parse_args()# Sklearn is VERY PICKY on how you put your values in...
    X = (
      np.array(
        [
          args["dataset_req"],

        ]
      ).astype("float").reshape(1, -1)
    )
    
    print("request is processed")
    print(X)
    if (X[0]==1):
      return {"class": 42, "chart_data": [5, 8, 2, 4, 6, 5, 8, 2, 4, 6]}
    elif (X[0]==2):
      return {"class": 42, "chart_data": [5, 2, 3, 5, 6, 1, 2, 3, 5, 6]}
    else:
      return {"class": 500, "chart_data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}


    


api.add_resource(Predict, "/predict")

if __name__ == "__main__":
    print("Starting server.")
    app.run(debug=True)
