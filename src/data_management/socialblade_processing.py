from pathlib import Path, PurePath
import time
import random
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import json
import numpy as np


def load_raw_data(data_path):
    print('Loading raw data.')
    raw_data = list()
    data_files = [f for f in data_path.glob('*.json')]
    t1 = time.time()
    for file in data_files:
        with file.open() as f:
            raw_data.extend(json.load(f))
    print('Loading finished in {:.2f} seconds.'.format(time.time()-t1))
    return raw_data


def extract_key_list(raw_data):
    key_list = list()
    for channel_dict in raw_data:
        for key in channel_dict.keys():
            if key not in key_list:
                key_list.append(key)
    return key_list


def sort_data(raw_data, key_list):
    print('Sorting the data into unified dictionaries.')
    data_dict = {key: [] for key in key_list}
    for channel_dict in raw_data:
        for (key, val) in channel_dict.items():
            if val:  # Some data lists are empty and need to be removed.
                val_x = list(map(int, val[0::2]))
                val_y = list(map(int, val[1::2]))
                data_dict[key].append([val_x, val_y])
    return data_dict


def remove_false_data(data_dict):
    print('Removing negative values from the data set.')
    for (key, val) in data_dict.items():
        if 'change' not in key:
            for idx, data in enumerate(val):
                val[idx] = smooth_out_negative_values(data)
    return data_dict


def smooth_out_negative_values(data):
    y_data = data[1]
    for idx, data_point in enumerate(y_data):
        if data_point < 0:
            y_data[idx] = y_data[idx-1] if not idx == 0 else 0
    return data


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


def merge_channel_data(data_dict):
    merged_dict = dict()
    for (key, val) in data_dict.items():
        merged_dict[key] = list()
        data_arr = get_data_array(key, val)
        for arr in val:
            for idx, el in enumerate(arr[0]):
                if el not in t_dict[key]:
                    t_dict[key].append(el)
    return t_dict


def get_min_max_time(array):
    t_min = 9999999999
    t_max = 0
    for sub_array in array:
        t_min = np.min(sub_array[0]) if np.min(sub_array[0]) < t_min else t_min
        t_max = np.max(sub_array[0]) if np.max(sub_array[0]) > t_max else t_max
    return t_min, t_max


def get_data_array(key, val):
    t_diff = 2592000 if 'monthly' in key else 604800
    t_min, t_max = get_min_max_time(val)
    t_max = np.round((t_max-t_min)/t_diff)*t_diff + t_min  # Get a matching discrete time step boundary.
    data_array = np.array(size=(2, (t_max-t_min)/t_diff))
    data_array[0] = np.arange(t_min, t_max + 1, t_diff)
    return data_array


def main():
    raw_data = load_raw_data(PATH)
    key_list = extract_key_list(raw_data)
    data_dict = sort_data(raw_data, key_list)
    df = pd.DataFrame.from_dict(raw_data)
    df.head()
    print('NO HEAD')
    data_dict = remove_false_data(data_dict)
    print('Press enter to inspect a new set, or any other key to finish.')
    while input() == '':
        show_data_subset(data_dict)
        print('Press enter to inspect a new set, or any other key to finish.')
    t_dict = merge_channel_data(data_dict)
    with open('timestamps.json', 'w') as f:
        json.dump(t_dict, f)


if __name__ == '__main__':
    sns.set(style="darkgrid")
    PATH = PurePath.joinpath(Path(__file__).resolve().parents[2], 'res', 'socialblade', 'raw')
    main()
    with open('timestamps.json', 'r') as f:
        t_dict = json.load(f)
    for key in t_dict.keys():
        print(key)
    arr = t_dict['daily-weekly-vidviews']
    arr = sorted(arr)
    plt.plot(arr)
    plt.show()
