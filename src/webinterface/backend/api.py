from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from pathlib import Path
import pandas as pd
from src.inference.model_comparison import get_predict_data as predictor

app = Flask(__name__)
CORS(app)

api = Api(app)  # Require a parser to parse our POST request.
parser = reqparse.RequestParser()
parser.add_argument("dataset_id_req")
parser.add_argument("ping")
parser.add_argument("selected_graph")
# Unpickle our model so we can use it!


# def load_data(data_folder_name, csv_file_name, type):
#     """
#     !@brief Opens a csv file starting from the folder 'res' and the input subfolders and extracts the data for the specified type
#     @param folder structure starting from the directory 'res' to the csv-file,
#     the name of the csv-file, 
#     type of the data to be extracted (name of column in csv)
#     @return extracted data in form of a list
#     """

#     # TODO: Remove test
#     # filePath = __file__
#     # print("This script file path is ", filePath)
#     # absFilePath = os.path.abspath(__file__)
#     # print("This script absolute path is ", absFilePath)

#     # Path to data directory
#     data_path = Path("../../../res/")
#     # Path to open CSV-file from
#     file_path = Path("{}/{}".format(data_folder_name, csv_file_name))
#     # Join the two partial paths to a complete path to access the file
#     complete_path = Path(data_path, file_path)

#     # Open file as a pandas frame
#     csv_file = pd.read_csv(complete_path)
#     # Convert the "Date" entries into datetime objects
#     csv_file["Date"] = pd.to_datetime(csv_file["Date"])
#     # Sort the pandas frame in the ascending date order
#     csv_file.sort_values(by=["Date"], inplace=True)
#     # Reconvert the datetime objects into Strings
#     csv_file["Date"] = csv_file["Date"].astype(str)
#     # Extract data of specified type to a list
#     data = csv_file[type].to_list()

#     return data


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

            # Switch statement depending on the requested dataset.
            # The allocation from the id to the lable (name) can be found in /.../allocation_datasets_id.CSV
            switch = switcher()
            dataset_lable = switch.dataset_switch(args["dataset_id_req"])

            # Use function to predict values and get raw and predicted data returned
            predicted_df, prophet_attr_df_post,  prophet_attr_df_pre,  prophet_dataframes_pre, prophet_dataframes_post = predictor(dataset_lable)

            # TODO: Expand comments
            # Unperdicted data
            datasets_unpredicted = [prophet_attr_df_pre, prophet_attr_df_post]
            result_unpredicted = pd.concat(datasets_unpredicted)
            result_unpredicted.reset_index(inplace=True)
            # Predicted data
            datasets_predicted = [prophet_attr_df_pre[dataset_lable], predicted_df]
            result_predicted = pd.concat(datasets_predicted)

            # Generate lists out of dataframes to send to frontend
            result_unpredicted_data = result_unpredicted[dataset_lable].to_list()
            result_predicted = result_predicted.to_list()
            result_dates = result_unpredicted["Date"].to_list()

            return {"class": 42,
                    "datecheck": 2,
                    "chart_data_1": result_unpredicted_data,
                    "chart_data_2": result_predicted,
                    "labels": result_dates,
                    "selected_graph": args["selected_graph"]
                    }

            # TODO: Catch case when no data returned?
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
