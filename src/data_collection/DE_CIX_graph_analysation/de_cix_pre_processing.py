"""!@brief Script to reformat csv file of DE-CIX data according to the already used format for other IX in this project.
@author Felix Montnacher
@date 06.07.2020
"""

import csv
from datetime import datetime
from pathlib import Path


def process_file(csv_file_name, new_file_name, data_unit_factor, ix_name, ix_type):
    """
    !@brief Generate a new csv-file with processed data from a csv-file with
    data from a graph.
    Opens and extracts the data from the input csv-file.
    Generates a new csv-file with the given name.
    Process raw data to usable data and add the input information.
    Write new lines with the specified format.
    @param Name of the CSV-file, name of the new file to generate,
    which factor to multiply datarate to receive b/s,
    name of the IX of the data, type of the ix.
    @return None
    """

    # CSV header for the new file
    header = ['ID', 'Timestamp', 'Date', 'bitrate', 'IX', 'type']

    # Open existing and unprocessed CSV file
    raw_folder = Path("raw/{}".format(csv_file_name))
    with open(raw_folder, 'rt') as raw_csv_file:
        csv_reader = csv.reader(raw_csv_file)

        # Open or create a new file
        # (Overwrites everything when file already exists)
        processed_folder = Path("processed/{}".format(new_file_name))
        with open(processed_folder, 'wt', newline='') as new_file:

            csv_writer = csv.writer(new_file)
            # write header
            csv_writer.writerow(header)

            # Loop trough every existing line in the CSV file
            for raw_line in csv_reader:
                formatted_raw_line = list()
                # Change seperation symbol from ";" to ","
                # (EXCEL default is ";")
                for item in raw_line:
                    split_list = list()
                    split_list = item.split(";")
                    # Add the new items in the split_list to the newLine
                    formatted_raw_line += split_list

                processed_line = list()

                # Add the ID
                processed_line.append(formatted_raw_line[0])
                # Add the Timestamp
                date = datetime.strptime(formatted_raw_line[2], "%d.%m.%Y")
                timestamp = datetime.timestamp(date)
                processed_line.append(timestamp)
                # Add the Date
                processed_line.append(date.date())
                # Add the bitrate
                processed_line.append(float(formatted_raw_line[1]) * data_unit_factor)
                # Add the IX
                processed_line.append(ix_name)
                # Add the type
                processed_line.append(ix_type)

                csv_writer.writerow(processed_line)


process_file("DE-CIX Dusseldorf_1_year.csv", "ix_dusseldorf_1_year.csv", 10**9, "ix_dusseldorf", "incoming")
process_file("DE-CIX Frankfurt_1_year.csv", "ix_Frankfurt_1_year.csv", 10**12, "ix_frankfurt", "incoming")
process_file("DE-CIX Hamburg_1_year.csv", "ix_Hamburg_1_year.csv", 10**9, "ix_hamburg", "incoming")
process_file("DE-CIX Munich_1_year.csv", "ix_Munich_1_year.csv", 10**9, "ix_munich", "incoming")
