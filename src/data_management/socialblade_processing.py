from pathlib import Path, PurePath
import time
import pandas as pd
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


def show_data_subset(raw_data, index):
    data_dict = raw_data[index]
    for key, val in data_dict.items():
        print('Data plot for {}'.format(key))
        val = list(map(int, val))
        x = val[0::2]
        y = val[1::2]
        print(x)
        print(y)
        sns.lineplot(x, y)


def main():
    raw_data = load_raw_data(PATH)
    for index in np.random.randint(0, len(raw_data)-1, 100):
        show_data_subset(raw_data, index)
    key_list = extract_key_list(raw_data)
    print(key_list)
    print(len(key_list))
    # read data
    # get all keys
    # inspect data samples
    # concat data set


if __name__ == '__main__':
    sns.set(style="whitegrid")
    PATH = PurePath.joinpath(Path(__file__).parents[2], 'res', 'socialblade', 'raw')
    main()

