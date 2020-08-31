from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from pathlib import Path
import pandas as pd
import datetime
import os
import sys
# sys.path.insert(0, '../../inference/')
# from model_comparison import get_predict_data as predictor
from src.inference.model_comparison import get_predict_data as predictor

app = Flask(__name__)
CORS(app)

api = Api(app)  # Require a parser to parse our POST request.
parser = reqparse.RequestParser()
parser.add_argument("dataset_id_req")
parser.add_argument("ping")
parser.add_argument("selected_graph")
# Unpickle our model so we can use it!


def load_data(data_folder_name, csv_file_name, type):
    """
    !@brief Opens a csv file starting from the folder 'res' and the input subfolders and extracts the data for the specified type
    @param folder structure starting from the directory 'res' to the csv-file,
    the name of the csv-file, 
    type of the data to be extracted (name of column in csv)
    @return extracted data in form of a list
    """

    # TODO: Remove test
    # filePath = __file__
    # print("This script file path is ", filePath)
    # absFilePath = os.path.abspath(__file__)
    # print("This script absolute path is ", absFilePath)

    # Path to data directory
    data_path = Path("../../../res/")
    # Path to open CSV-file from
    file_path = Path("{}/{}".format(data_folder_name, csv_file_name))
    # Join the two partial paths to a complete path to access the file
    complete_path = Path(data_path, file_path)

    # TODO: remove Test
    # complete_path = Path(filePath, data_path, file_path)
    # print(complete_path)

    # Open file as a pandas frame
    csv_file = pd.read_csv(complete_path)
    # Convert the "Date" entries into datetime objects
    csv_file["Date"] = pd.to_datetime(csv_file["Date"])
    # Sort the pandas frame in the ascending date order
    csv_file.sort_values(by=["Date"], inplace=True)
    # Reconvert the datetime objects into Strings
    csv_file["Date"] = csv_file["Date"].astype(str)
    # Extract data of specified type to a list
    data = csv_file[type].to_list()

    return data


class switcher():
    def dataset_switch(self, dataset_id):
        default = "incorrect dataset"
        # getattr returns function from within the class, matching to 'dataset_id'
        # lambda gets returned, if not matching class was found
        return getattr(self, 'dataset_' + str(dataset_id), lambda: default)()

    def dataset_0(self):
        return "ix_bitrate"

    def dataset_1(self):
        return "test1"

    def dataset_2(self):
        return "test2"


class Predict(Resource):
    def post(self):
        args = parser.parse_args()  # Sklearn is VERY PICKY on how you put your values in...

        print("\n---New request is processed---")
        print("Args: {}".format(args))

        if (args["ping"] == "1"):
            print("answered keep-alive")
            return {"alive": 1}
        else:
            # Print for checking parameter during development
            print("Received 'selected_graph' paramter: {}".format(args["selected_graph"]))

            # TODO: Switch
            # Switch statement depending on the requested dataset.
            # The allocation from the id to the lable (name) can be found in /.../allocation_datasets_id.CSV
            switch = switcher()
            # print(switch.dataset_switch(0))
            # TODO: !! Change 0 to dataset_id_req !!
            dataset_lable = switch.dataset_switch(0)

            # Use function to predict values and get raw and predicted data returned
            dataset_data = predictor.get_predict_data(dataset_lable)
            print(dataset_data)
            
            # return {"class": 42,
            #             "datecheck": 2,
            #             "chart_data_1": covid_deaths,
            #             "chart_data_2": covid_confirmed,
            #             "labels": covid_dates,
            #             "selected_graph": args["selected_graph"]
            #             }
            # if (args["dataset_id_req"] == '1'):
            #     return {"class": 42,
            #             "datecheck": 2,
            #             "chart_data_1": covid_deaths,
            #             "chart_data_2": covid_confirmed,
            #             "labels": covid_dates,
            #             "selected_graph": args["selected_graph"]
            #             }
            # elif (args["dataset_id_req"] == '2'):
            #     return {"class": 42,
            #             "datecheck": 2,
            #             "chart_data_1": [0, 0, 0, 5, 6, 1, 2, 3, 5, 6],
            #             "chart_data_2": [5, 8, 2, 4, 6, 5, 8, 2, 4, 6],
            #             "labels": [1, 2, 3, 4, 5, 6, 7, 8, 9],
            #             "selected_graph": args["selected_graph"]
            #             }
            # else:
            #     return {"class": 500,
            #             "datecheck": 2,
            #             "chart_data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            #             "chart_data_2": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            #             "labels": [1, 2, 3, 4, 5, 6, 7, 8, 9],
            #             }


api.add_resource(Predict, "/predict")


def main():
    print("Starting server.")
    app.run(debug=True, host="0.0.0.0")


if __name__ == "__main__":
    main()
