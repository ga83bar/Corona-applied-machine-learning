"""!@brief Pipeline visualizer classes. Used for visualizing data as needed during the pipeline.
@file Pipeline visualizer classes file.
@author Martin Schuck
@date 18.07.2020
"""

import os
import pandas as pd
import datetime as dt


class PipelinePlotter:

    def __init__(self, plot):
        self.plot = plot

    def fit(self, x, y):
        """
        Has to be implemented in order to work with sklearn's pipeline object.
        """
        return self

    def transform(self, x):
        """
        Has to be named transform in order to work with the pipeline. We want an all in one solution, so our data
        analysis is integrated into the whole pipeline process. Transform in this context is no transform, but a plot.
        """
        if self.plot:
            split_data_dict = self.split_data(x)
            self.plot_apple(split_data_dict['apple'])
            self.plot_covid(split_data_dict['covid'])
            self.plot_ix(split_data_dict['ix'])
            self.plot_playstation(split_data_dict['playstation'])
            self.plot_socialblade(split_data_dict['socialblade'])
            self.plot_steam(split_data_dict['steam'])
            self.plot_twitch(split_data_dict['twitch'])
        return x

    def plot_apple(self, apple_frame):
        """
        ### TODO: IMPLEMENT @Henrique ###
        """
        raise NotImplementedError

    def plot_covid(self, covid_frame):
        """
        ### TODO: IMPLEMENT @MIKE ###
        """
        raise NotImplementedError

    def plot_ix(self, ix_frame):
        """
        ### TODO: IMPLEMENT @ARON ###
        """
        raise NotImplementedError

    def plot_playstation(self, playstation_frame):
        """
        ### TODO: IMPLEMENT @MIKE ###
        """
        raise NotImplementedError

    def plot_socialblade(self, socialblade_frame):
        """
        ### TODO: IMPLEMENT @MARTIN ###
        """
        raise NotImplementedError

    def plot_steam(self, steam_frame):
        """
        ### TODO: IMPLEMENT @MIKE ###
        """
        raise NotImplementedError

    def plot_twitch(self, twitch_frame):
        """
        ### TODO: IMPLEMENT @MARTIN ###
        """
        raise NotImplementedError

    @staticmethod
    def split_data(x):
        """
        Splits the data into the individual components and returns the dictionary of split pandas frames.
        """
        split_data_dict = dict()
        split_data_dict['apple'] = pd.concat([x['Date']], axis=1)
        split_data_dict['covid'] = pd.concat([x['Date'], x['deaths'], x['confirmed'], x['recovered'], x['active'],
                                              x['new_confirmed'], x['new_recovered'], x['new_deaths']], axis=1)
        split_data_dict['ix'] = pd.concat([x['Date'], x['bitrate']], axis=1)
        split_data_dict['playstation'] = pd.concat([x['Date'], x['PS3'], x['PS4'], x['Vita']], axis=1)
        split_data_dict['socialblade'] = pd.concat([x['Date'], x['weekly_views'], x['weekly_sub']], axis=1)
        split_data_dict['steam'] = pd.concat([x['Date'], x['Users'], x['In-Game']], axis=1)
        split_data_dict['twitch'] = pd.concat([x['Date'], x['av_conc_viewers'], x['av_conc_channels'],
                                               x['time_watched'], x['active_streamers']], axis=1)
        return split_data_dict


class DataMerger(object):
    def __init__(self, folder_list=None):

        # make a list containing all paths to processed data
        if folder_list is None:
            folders = ['covid', 'de-cix', 'ix', 'playstation',
                       'socialblade', 'steam', 'twitch']
        else:
            folders = folder_list

        # join the paths structure ~ ./res/'folder_name'/processed
        path_to_res = os.path.join('.', 'res')
        self.path_to_processed = []

        for folder in folders:
            path = os.path.join(path_to_res, folder, 'processed')
            self.path_to_processed.append(path)

        # init other attributes
        self.frame = pd.DataFrame()

    def get_all_data(self, start_date=None, end_date=None):
        if isinstance(start_date, dt.datetime) and isinstance(end_date, dt.datetime):
            self.frame = self.__get_date_frame(start_date, end_date)
        else:
            start = dt.datetime(2019, 8, 1)
            end = dt.datetime(2020, 6, 15)
            print('\x1b[0;30;41m' + 'DataMerger.get_all_data dates are not valid !!' +
                  'Take default values \nStart\t {}'.format(start) +
                  '\nEnd\t {}'.format(end) + '\x1b[0m')
            self.frame = self.__get_date_frame(start, end)

        for folder in self.path_to_processed:
            dirs = os.listdir(folder)
            for file in dirs:
                if file.endswith('.csv'):
                    path_processed_data = os.path.join(folder, file)
                    df_tmp = pd.read_csv(path_processed_data)
                    df_tmp['Date'] = pd.to_datetime(df_tmp['Date'], utc=True)
                    self.frame = self.frame.merge(df_tmp, how='left')
                    # print(self.frame.head())
                    # print(self.frame.describe())

        return self.frame

    def __get_date_frame(self, start, end):
        """ Gen list of all dates between start and end date"""
        date_list = [start + dt.timedelta(days=x) for x in range(0, (end - start).days)]
        frame = pd.DataFrame(date_list)
        frame.columns = ['Date']
        frame['Date'] = pd.to_datetime(frame['Date'], utc=True)
        return frame


def test():
    da_m = DataMerger()
    st = dt.datetime(2017, 1, 1)
    end = dt.datetime(2020, 6, 15)
    frame = da_m.get_all_data(st)

if __name__ == '__main__':
    test()
