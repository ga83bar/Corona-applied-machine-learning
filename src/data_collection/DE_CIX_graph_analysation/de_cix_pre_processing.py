import csv
from datetime import datetime
from pathlib import Path

def processFile(csvFileName, newFileName, dataUnitFactor, ixName, ixType):
    """
    !@brief Generate a new csv-file with processed data from a csv-file with data from a graph.
    
    Opens and extracts the data from the input csv-file, 
    generates a new csv-file with the given name, 
    process raw data to usable data and add the input information,
    write new lines with the specified format.

    @param Name of the CSV-file, name of the new file to generate, which factor to multiply datarate to receive b/s, name of the IX of the data, type of the ix.
    @return None
    """

    #CSV header for the new file
    header = ['ID', 'Timestamp', 'Date', 'bitrate', 'IX', 'type']

    #Open existing and unprocessed CSV file
    raw_folder = Path("raw/{}".format(csvFileName))
    with open(raw_folder, 'rt') as rawCsvFile:
        csv_reader = csv.reader(rawCsvFile)

        #Open or create a new file (Overwrites everything when file already exists)
        processed_folder = Path("processed/{}".format(newFileName))
        with open(processed_folder, 'wt', newline='') as newFile:

            csv_writer = csv.writer(newFile)
            # write header
            csv_writer.writerow(header) 

            #Loop trough every existing line in the CSV file
            for rawLine in csv_reader:
                
                formattedRawLine = list()
                #Change seperation symbol from ";" to "," (EXCEL default is ";")
                for item in rawLine:  
                    splitList = list()
                    splitList = item.split(";")
                    #Add the new items in the splitList to the newLine
                    formattedRawLine += splitList

                processedLine = list()

                #Add the ID
                processedLine.append(formattedRawLine[0])
                #Add the Timestamp
                date = datetime.strptime(formattedRawLine[2], "%d.%m.%Y")
                timestamp = datetime.timestamp(date)
                processedLine.append(timestamp)
                #Add the Date
                processedLine.append(date.date())
                #Add the bitrate
                processedLine.append(float(formattedRawLine[1]) * dataUnitFactor)
                #Add the IX
                processedLine.append(ixName)
                #Add the type
                processedLine.append(ixType)

                csv_writer.writerow(processedLine)

processFile("DE-CIX Dusseldorf_1_year.csv", "ix_dusseldorf_1_year.csv", 10**9, "ix_dusseldorf", "incoming")
processFile("DE-CIX Frankfurt_1_year.csv", "ix_Frankfurt_1_year.csv", 10**12, "ix_frankfurt", "incoming")
processFile("DE-CIX Hamburg_1_year.csv", "ix_Hamburg_1_year.csv", 10**9, "ix_hamburg", "incoming")
processFile("DE-CIX Munich_1_year.csv", "ix_Munich_1_year.csv", 10**9, "ix_munich", "incoming")