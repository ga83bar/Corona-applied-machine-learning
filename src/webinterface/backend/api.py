from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from pathlib import Path
import pandas as pd
import datetime

app = Flask(__name__)
CORS(app)

api = Api(app)  # Require a parser to parse our POST request.
parser = reqparse.RequestParser()
parser.add_argument("dataset_req")
parser.add_argument("start_date_req")
parser.add_argument("end_date_req")
parser.add_argument("ping")
# Unpickle our model so we can use it!


def load_data(data_folder_name, csv_file_name, type):
    """
    !@brief Opens a csv file starting from the folder 'res' and the input subfolders and extracts the data for the specified type
    @param folder structure starting from the directory 'res' to the csv-file,
    the name of the csv-file, 
    type of the data to be extracted (name of column in csv)
    @return extracted data in form of a list
    """

    # Path to data directory
    data_path = Path("../../../res/")
    # Path to open CSV-file from
    file_path = Path("{}/{}".format(data_folder_name, csv_file_name))
    # Join the two partial paths to a complete path to access the file
    complete_path = Path(data_path, file_path)

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


class Predict(Resource):
    def post(self):
        args = parser.parse_args()  # Sklearn is VERY PICKY on how you put your values in...

        print(args)
        if (args["ping"] == "1"):
            print("answered keep-alive")
            return {"alive": 1}
        else:
            print("\nrequest is processed")
            print(args["dataset_req"])
            print(args["start_date_req"])
            print(args["end_date_req"])

            covid_dates = load_data("covid/processed", "covid.csv", "Date")
            covid_deaths = load_data("covid/processed", "covid.csv", "deaths")
            covid_confirmed = load_data("covid/processed", "covid.csv", "confirmed")
            start_date = datetime.datetime.strptime(args["start_date_req"], '%Y-%m-%d')
            end_date = datetime.datetime.strptime(args["end_date_req"], '%Y-%m-%d')
            
            if (start_date > end_date):
                return {"class": 42,
                        "datecheck": 1,
                        "chart_data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        "chart_data_2": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        "labels": [1, 2, 3, 4, 5, 6, 7, 8, 9]
                        }
            if (args["dataset_req"] == '1'):
                return {"class": 42,
                        "datecheck": 2,
                        "chart_data_1": covid_deaths,
                        "chart_data_2": covid_confirmed,
                        "labels": covid_dates
                        }
            elif (args["dataset_req"] == '2'):
                return {"class": 42,
                        "datecheck": 2,
                        "chart_data_1": [5, 2, 3, 5, 6, 1, 2, 3, 5, 6],
                        "chart_data_2": [5, 8, 2, 4, 6, 5, 8, 2, 4, 6],
                        "labels": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                        }
            else:
                return {"class": 500,
                        "datecheck": 2,
                        "chart_data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        "chart_data_2": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        "labels": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                        }


api.add_resource(Predict, "/predict")

if __name__ == "__main__":
    print("Starting server.")
    app.run(debug=True, host="0.0.0.0")
