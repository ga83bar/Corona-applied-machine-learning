import os
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

api = Api(app)# Require a parser to parse our POST request.
parser = reqparse.RequestParser()
parser.add_argument("sepal_length")
parser.add_argument("sepal_width")
parser.add_argument("petal_length")
parser.add_argument("petal_width")# Unpickle our model so we can use it!

class Predict(Resource):
  def post(self):
    args = parser.parse_args()# Sklearn is VERY PICKY on how you put your values in...
    X = (
      np.array(
        [
          args["sepal_length"],
          args["sepal_width"],
          args["petal_length"],
          args["petal_width"]
        ]
      ).astype("float").reshape(1, -1)
    ) 
    print("request is processed")
    
    return {"class": 42}
    
api.add_resource(Predict, "/predict")

if __name__ == "__main__":
    print("Starting server.")
    app.run(debug=True)
