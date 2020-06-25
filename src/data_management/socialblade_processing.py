from pathlib import Path, PurePath
import random
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import json
import numpy as np


def load_raw_data(data_path):
    raw_data = list()
    data_files = [f for f in data_path.glob('*.json')]
    for file in data_files:
        with file.open() as f:
            raw_data.extend(json.load(f))
    return raw_data


def extract_key_list(raw_data):
    key_list = list()
    for channel_dict in raw_data:
        for key in channel_dict.keys():
            if key not in key_list:
                key_list.append(key)
    return key_list


def sort_data(raw_data, key_list):
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
    for key, val in data_dict.items():
        idx = random.randint(0, len(val))
        x = [datetime.fromtimestamp(d/1000) for d in val[idx][0]]
        y = val[idx][1]

        plt.subplots(figsize=(13, 5))
        # Format axis ticks
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        sns.lineplot(x, y)
        plt.gcf().autofmt_xdate()
        plt.xlabel('Time')
        plt.ylabel(key)
        plt.show()


def create_month_df(data_dict, key, drop=False):
    m_data = data_dict[key]
    series = pd.Series(m_data[1], pd.to_datetime(m_data[0], unit='s'))
    if drop:
        series = series[series > 0]
    series_rs = series.resample('1MS').sum()
    series_cnt = series.resample('1MS').count()
    df = pd.DataFrame({'Date': series_cnt.keys(), 'Views': series_rs.values, 'Accounts': series_cnt.values})
    df.head()
    return df


def create_week_df(data_dict, key, drop=False):
    m_data = data_dict[key]
    series = pd.Series(m_data[1], pd.to_datetime(m_data[0], unit='s'))
    if drop:
        series = series[series > 0]
    series_rs = series.resample('1W').sum()
    series_cnt = series.resample('1W').count()
    df = pd.DataFrame({'Date': series_cnt.keys(), 'Views': series_rs.values, 'Accounts': series_cnt.values})
    df.head()
    return df


def plot_df(df, title):
    fig, ax = plt.subplots(figsize=(10, 10))
    # Add x-axis and y-axis
    sns.lineplot(df['Date'],
                 df['Views']/df['Accounts'],
                 color='purple')
    # Set title and labels for axes
    ax.set(xlabel="Date",
           ylabel="Views",
           title=title)
    plt.show()


def clean_df(df):
    date_2018 = 1512000000  # Date of 1.1.2018 in UNIX seconds timestamp style.
    idx = df[df['Date'].astype(np.int64) / 10 ** 9 < date_2018].index
    df.drop(idx, inplace=True)
    idx = df[df['Views'] == 0].index
    df.drop(idx, inplace=True)


def main():
    print('Loading raw data.')
    raw_data = load_raw_data(PurePath.joinpath(PATH, 'raw'))
    print('Sorting the data into unified dictionaries.')
    data_dict = sort_data(raw_data, extract_key_list(raw_data))
    df_list = list()
    print('Creating pandas data frames.')
    for key in data_dict.keys():
        if 'change' in key:
            df = create_week_df(data_dict, key, drop=False)
        elif 'month' in key:
            df = create_month_df(data_dict, key, True)
        else:
            df = create_week_df(data_dict, key, drop=True)
        df.name = str(key)
        df_list.append(df)
    print('Cleaning data frames.')
    for df in df_list:
        clean_df(df)
    print('Plotting data frames for inspection.')
    for df in df_list:
        plot_df(df, title=df.name)
    print('Saving data frames into processed folder.')
    for df in df_list:
        df.to_csv(PurePath.joinpath(PATH, 'processed', df.name + '.csv').as_posix(), encoding='utf-8', index=False)
    print('Saving complete, script will exit.')


if __name__ == '__main__':
    sns.set(style="darkgrid")
    PATH = PurePath.joinpath(Path(__file__).resolve().parents[2], 'res', 'socialblade')
    main()
