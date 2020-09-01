from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
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
    """
    !@brief Implemets a switch-case function in python to select the right dataset name for a specified ID
    @param Generate an insstance of the switcher class and use the id of an dataset as an in in the dataset_switch function
    @return For the specified integer ID in the dataset_swicht function, the name of the according dataset gets returned as a string
    """
    def dataset_switch(self, dataset_id):
        default = "incorrect dataset"
        # getattr returns function from within the class, matching to 'dataset_id'
        # lambda gets returned, if not matching class was found
        return getattr(self, 'dataset_' + str(dataset_id), lambda: default)()

    def dataset_0(self):
        return "ix_bitrate"

    def dataset_1(self):
        return "youtube_viewchange"

    def dataset_2(self):
        return "youtube_views"

    def dataset_3(self):
        return "steam_users"

    def dataset_4(self):
        return "steam_ingame"

    def dataset_5(self):
        return "twitch_views"

    def dataset_6(self):
        return "twitch_channels"

    def dataset_7(self):
        return "twitch_viewtime"

    def dataset_8(self):
        return "twitch_streams"

    def dataset_9(self):
        return "ps_users"

    def dataset_10(self):
        return "stock_med"

    def dataset_11(self):
        return "stock_bank"

    def dataset_12(self):
        return "stock_energy"

    def dataset_13(self):
        return "stock_oil"

    def dataset_14(self):
        return "stock_steel"

    def dataset_15(self):
        return "stock_automotive"

    def dataset_16(self):
        return "stock_telecom"

    def dataset_17(self):
        return "stock_tech"


class Predict(Resource):
    def post(self):
        """
        !@brief Is getting called, when a http request has been received.
        The content gets extracted and either a ping-return is sent or a ML-Model is loaded
        and predicts data for a requested dataset, which will be returned.
        """

        args = parser.parse_args()  # Sklearn is VERY PICKY on how you put your values in...

        print("\n---New request is processed---")
        print("Args: {}".format(args))

        if (args["ping"] == "1"):
            print("answered keep-alive")
            return {"alive": 1}
        else:
            # Print for checking parameter during development
            print("Received 'selected_graph' paramter: {}".format(args["selected_graph"]))

            # Switch statement depending on the requested dataset to reiceive the dataset name out of it´s ID.
            # The allocation from the id to the lable (name) can be found in /.../allocation_datasets_id.CSV
            switch = switcher()
            dataset_lable = switch.dataset_switch(args["dataset_id_req"])

            # Use function to predict values and get raw and predicted data returned
            predicted_df, prophet_attr_df_post,  prophet_attr_df_pre = predictor(dataset_lable)

            # Unpredicted data is processed
            # Received data is merged together with data up to and after the 1.1.2020.
            # Drop last row to not use it twice
            prophet_attr_df_pre = prophet_attr_df_pre.drop(prophet_attr_df_pre.index[-1])
            datasets_unpredicted = [prophet_attr_df_pre, prophet_attr_df_post]
            result_unpredicted = pd.concat(datasets_unpredicted)
            result_unpredicted.reset_index(inplace=True)

            # Get the index of the 2020-01-01 (where the rpediction starts)
            index_prediction_start = result_unpredicted.loc[result_unpredicted["Date"] == "2020-01-01"].index.item()

            # Predicted data processed
            # Change data type into pandas series
            result_predicted = pd.Series(predicted_df)

            # Generate lists out of dataframes to send to frontend
            complete_unpredicted_data = result_unpredicted[dataset_lable].to_list()
            complete_model_data = result_predicted.to_list()
            complete_predicted_data = result_predicted.to_list()
            result_dates = result_unpredicted["Date"].to_list()

            for i in range(index_prediction_start, len(complete_model_data)):
                complete_model_data[i] = None

            for i in range(0, index_prediction_start - 1):
                complete_predicted_data[i] = None

            # The return statement will be sent to the frontend.
            return {"class": 42,
                    "datecheck": 2,
                    "chart_data_1": complete_unpredicted_data,
                    "chart_data_2": complete_model_data,
                    "chart_data_3": complete_predicted_data,
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
