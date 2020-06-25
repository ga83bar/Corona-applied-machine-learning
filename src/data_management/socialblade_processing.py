"""!@brief Socialblade preprocessing script. Reads raw data, processes it with pandas and saves it into csv files.
@details Data is cleaned from wrong entries such as negative view counts and resampled with pandas. Includes options
to show plots for samples of the raw data as well as the final resulting data sets. Stores the data processed data to
the res/socialblade/processed folder.
@file Socialblade preprocessing script file.
@author Martin Schuck
@date 25.6.2020
"""

from pathlib import Path, PurePath
import random
import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np


def load_raw_data(data_path):
    """!@brief Loads the raw data from the scraper.

    Data is expected to be in the format as returned by the sb_scraper containers. All result files should be in a
    single folder.
    @warning No other json files should be in the folder!
    @param data_path File path to the raw data save folder.
    @return Returns the list of loaded raw data chunks returned by the work packages of the scraper.
    """
    raw_data = list()
    data_files = data_path.glob('*.json')
    for file in data_files:
        with file.open() as f:
            raw_data.extend(json.load(f))
    return raw_data


def extract_key_list(raw_data):
    """!@brief Extracts all keys present in the raw data.

    @param raw_data The unprocessed, loaded data from the scrapers.
    @return Returns a list of all unique keys present in the raw data.
    """
    key_list = list()
    for channel_dict in raw_data:
        for key in channel_dict.keys():
            if key not in key_list:
                key_list.append(key)
    return key_list


def sort_data(raw_data, key_list):
    """!@brief Extracts all keys present in the raw data.

    @param raw_data The unprocessed, loaded data from the scrapers.
    @param key_list The list of all unique keys present in the raw data.
    @return Returns the restructured data as a dictionary of unique keys with all their data as value.
    """
    data_dict = {key: [[], []] for key in key_list}
    for channel_dict in raw_data:
        for (key, val) in channel_dict.items():
            if val:  # Some data lists are empty and need to be removed.
                val_x = list(map(int, val[0::2]))
                val_x = [int(x/1000) for x in val_x]  # Times are in ms, should be s for conversion though.
                val_y = list(map(int, val[1::2]))
                data_dict[key][0].extend(val_x)
                data_dict[key][1].extend(val_y)
    return data_dict


def show_data_subset(data_dict):
    """!@brief Shows a subset of raw data.

    Each key category is plotted once. Data for each key is randomly chosen among all available data for this particular
    key. Uses a seaborn lineplot.
    @warning Individual plots DO NOT belong to the same channel!
    @param data_dict The data sorted into a dictionary by the sort_data function.
    """
    for key, val in data_dict.items():
        idx = random.randint(0, len(val))
        x_axis = [datetime.fromtimestamp(d/1000) for d in val[idx][0]]
        y_axis = val[idx][1]

        plt.subplots(figsize=(13, 5))
        # Format axis ticks
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        sns.lineplot(x_axis, y_axis)
        plt.gcf().autofmt_xdate()
        plt.xlabel('Time')
        plt.ylabel(key)
        plt.show()


def create_month_df(data_dict, key, drop=False):
    """!@brief Creates a pandas data frame from the data dictionary resampled into monthly bins.

    Resamples the time series in the data into monthly bins and sums them up. To assess how to weight the data, also
    includes the number of channels that contributed per month. Optionally drops negative view counts.
    @param data_dict The data sorted into a dictionary by the sort_data function.
    @param key The key to specify which data arrays to use for data frame creation.
    @param drop Flag to drop negative values from the time series.
    @return Returns the assembled data as a pandas data frame.
    """
    m_data = data_dict[key]
    series = pd.Series(m_data[1], pd.to_datetime(m_data[0], unit='s'))
    if drop:
        series = series[series > 0]
    series_rs = series.resample('1MS').sum()
    series_cnt = series.resample('1MS').count()
    data_frame = pd.DataFrame({'Date': series_cnt.keys(), 'Views': series_rs.values, 'Accounts': series_cnt.values})
    return data_frame


def create_week_df(data_dict, key, drop=False):
    """!@brief Creates a pandas data frame from the data dictionary resampled into weekly bins.

    Resamples the time series in the data into weekly bins and sums them up. To assess how to weight the data, also
    includes the number of channels that contributed per week. Optionally drops negative view counts.
    @param data_dict The data sorted into a dictionary by the sort_data function.
    @param key The key to specify which data arrays to use for data frame creation.
    @param drop Flag to drop negative values from the time series.
    @return Returns the assembled data as a pandas data frame.
    """
    m_data = data_dict[key]
    series = pd.Series(m_data[1], pd.to_datetime(m_data[0], unit='s'))
    if drop:
        series = series[series > 0]
    series_rs = series.resample('1W').sum()
    series_cnt = series.resample('1W').count()
    data_frame = pd.DataFrame({'Date': series_cnt.keys(), 'Views': series_rs.values, 'Accounts': series_cnt.values})
    return data_frame


def plot_df(data_frame, title):
    """!@brief Plots the data frame.

    Uses the seaborn line plot to plot the data presented by the data frame. Views are inversly weighted by the number
    of accounts contributing towards them.
    @param data_frame Pandas data frame to plot.
    @param title The plot title.
    """
    _, axis = plt.subplots(figsize=(10, 10))
    sns.lineplot(data_frame['Date'],
                 data_frame['Views']/data_frame['Accounts'],
                 color='purple')
    axis.set(xlabel="Date",
             ylabel="Views/Accounts",
             title=title)
    plt.show()


def clean_df(data_frame):
    """!@brief Cleans the pandas data frame.

    Removes all data with timestamps from earlier than 1.1.2018 since the old data is extremely noisy/sparse. Also drops
    all data entries with 0 Views/Subscribers.
    @warning This is an inplace function! Input objects will be modified!
    @param data_frame Pandas data frame to process.
    """
    date_2018 = 1512000000  # Date of 1.1.2018 in UNIX seconds timestamp style.
    idx = data_frame[data_frame['Date'].astype(np.int64) / 10 ** 9 < date_2018].index
    data_frame.drop(idx, inplace=True)
    idx = data_frame[data_frame['Views'] == 0].index
    data_frame.drop(idx, inplace=True)


def main():
    """!@brief Loads the raw data, processes it and stores it.
    """
    print('Loading raw data.')
    raw_data = load_raw_data(PurePath.joinpath(PATH, 'raw'))
    print('Sorting the data into unified dictionaries.')
    data_dict = sort_data(raw_data, extract_key_list(raw_data))
    df_list = list()
    print('Creating pandas data frames.')
    for key in data_dict.keys():
        if 'change' in key:
            data_frame = create_week_df(data_dict, key, drop=False)
        elif 'month' in key:
            data_frame = create_month_df(data_dict, key, True)
        else:
            data_frame = create_week_df(data_dict, key, drop=True)
        data_frame.name = str(key)
        df_list.append(data_frame)
    print('Cleaning data frames.')
    for data_frame in df_list:
        clean_df(data_frame)
    print('Plotting data frames for inspection.')
    for data_frame in df_list:
        plot_df(data_frame, title=data_frame.name)
    print('Saving data frames into processed folder.')
    for data_frame in df_list:
        data_frame.to_csv(PurePath.joinpath(PATH, 'processed', data_frame.name + '.csv').as_posix(),
                          encoding='utf-8', index=False)
    print('Saving complete, script will exit.')


if __name__ == '__main__':
    sns.set(style="darkgrid")
    PATH = PurePath.joinpath(Path(__file__).resolve().parents[2], 'res', 'socialblade')
    main()
