"""!@brief Pipeline to process the gathered data from our sources.
@details Scales the data, computes running averages for time series where deemed appropriate and saves the scaled data
set into two files. One contains all data prior to the corona pandemic start (which we determined to be at 01.01.2020),
and the other one all data points from during the pandemic.
@file Data pipeline file.
@author Martin Schuck
@date 11.8.2020
"""


from pathlib import Path
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import sector_tuple_list, index_codes


def pipeline(verbose=False, plot=False):
    """!@brief Pipeline process to filter, process, sum and scale the raw data.

    Saves the resulting data frames into two files at /res/pipeline.

    @param verbose Toggles verbose output over the terminal.
    @param plot Toggles the analysing plots. Plots can be time consuming to display. Switch off for better performance.
    """
    # Load the raw data set and clean dirty columns.
    df = load_data_set(verbose=verbose)

    # Get the data frame index for 01.01.2020 to separate pre and post corona data.
    end_date = '2020-01-01'
    end_index = df.index[(df['Date'] == end_date).values][0]

    # Execute processing steps.
    df_processing(df, plot=plot)
    # Clean data frame and rename into a unified naming scheme.
    clean_df(df)
    if verbose:
        df.info()
    # Split data set into a pre corona data set and a corona data set. Scale both appropriately.
    scaled_pre_corona_df, scaled_corona_df, scaler = scale_split_df(df, end_index=end_index)
    if plot:
        fig = plt.figure(figsize=(24, 24))
        ax = fig.add_axes([0, 0, 1, 1])
        pd.plotting.scatter_matrix(scaled_pre_corona_df, ax=ax)
        plt.show()
        fig = plt.figure(figsize=(24, 24))
        ax = fig.add_axes([0, 0, 1, 1])
        pd.plotting.scatter_matrix(scaled_corona_df, ax=ax)
        plt.show()

    # Save data frame.
    save_df(scaled_pre_corona_df, scaled_corona_df, scaler)


def load_data_set(verbose=False):
    """!@brief Loads the raw data frame from the resource folder.

    @param verbose Toggles verbose output over the terminal.
    """
    root = Path().absolute().parent.parent
    dataset_path = root.joinpath('res', 'all_raw.csv')

    df = pd.read_csv(dataset_path)
    if verbose:
        df.info()

    df.drop('Unnamed: 0', axis=1, inplace=True)
    df.drop('Unnamed: 0.1', axis=1, inplace=True)
    df['Date'] = df['Date'].apply(lambda x: x[:-15])  # Drop the UTC string part.
    return df


def df_processing(df, plot=False):
    """!@brief Runs the individual processing steps for the data.

    @param df The data frame to process.
    @param plot Toggles the analysing plots. Plots can be time consuming to display. Switch off for better performance.
    """
    processing_collection = [corona_processing, ix_processing, playstation_processing, steam_processing,
                             twitch_processing, socialblade_processing, stock_processing]
    for function in processing_collection:
        function(df, plot=plot)


def corona_processing(df, plot):
    """!@brief Corona processing function.

    @param df The data frame to process.
    @param plot Toggles the analysing plots. Plots can be time consuming to display. Switch off for better performance.
    """
    df['deaths'].fillna(0, inplace=True)
    df['recovered'].fillna(0, inplace=True)
    df['active'].fillna(0, inplace=True)
    df['confirmed'].fillna(0, inplace=True)
    df['new_confirmed'].fillna(0, inplace=True)
    df['new_recovered'].fillna(0, inplace=True)
    df['new_deaths'].fillna(0, inplace=True)
    if plot:
        corona_processing_plot(df)


def corona_processing_plot(df):
    """!@brief Plots the results from the corona processing.

    @param df The data frame to use for plotting.
    """
    covid_df = df.melt('Date', value_vars=['deaths', 'recovered', 'active', 'confirmed', 'new_confirmed',
                                           'new_recovered', 'new_deaths'],
                       var_name='cols', value_name='vals')
    g = sns.lineplot(x="Date", y="vals", hue='cols', data=covid_df)
    g.set_xticks(np.arange(0, len(df['Date']), 300))
    g.plot()
    plt.show()


def ix_processing(df, plot):
    """!@brief IX processing function.

    @param df The data frame to process.
    @param plot Toggles the analysing plots. Plots can be time consuming to display. Switch off for better performance.
    """
    df['bitrate'] = df['bitrate'].rolling(7, win_type='triang', min_periods=1).sum()
    if plot:
        ix_processing_plot(df)


def ix_processing_plot(df):
    """!@brief Plots the results from the IX processing.

    @param df The data frame to use for plotting.
    """
    ix_df = df.melt('Date', value_vars=['bitrate'], var_name='cols', value_name='vals')

    g = sns.lineplot(x="Date", y="vals", hue='cols', data=ix_df)
    g.set_xticks(np.arange(0, len(df['bitrate']), 300))
    g.plot()
    plt.show()


def playstation_processing(df, plot):
    """!@brief Playstation processing function.

    @param df The data frame to process.
    @param plot Toggles the analysing plots. Plots can be time consuming to display. Switch off for better performance.
    """
    ps_keys = ['PS3', 'PS4', 'Vita']
    if all(key in df.keys() for key in ps_keys):
        df['PS'] = df['PS3'] + df['PS4'] + df['Vita']
        df.drop('PS3', axis=1, inplace=True)
        df.drop('PS4', axis=1, inplace=True)
        df.drop('Vita', axis=1, inplace=True)
        # Smooth time series with rolling average.
        df['PS'] = df['PS'].rolling(7, win_type='triang', min_periods=1).sum()
    else:
        print('Warning: Keys not present in playstation_processing in src/data_pipeline/pipeline.py')
    if plot:
        playstation_processing_plot(df)


def playstation_processing_plot(df):
    """!@brief Plots the results from the playstation processing.

    @param df The data frame to use for plotting.
    """
    ps_df = df.melt('Date', value_vars=['PS'], var_name='cols', value_name='vals')

    g = sns.lineplot(x="Date", y="vals", hue='cols', data=ps_df)
    g.set_xticks([0, 600, 1200])
    g.plot()
    plt.show()


def steam_processing(df, plot):
    """!@brief Steam processing function.

    @param df The data frame to process.
    @param plot Toggles the analysing plots. Plots can be time consuming to display. Switch off for better performance.
    """
    df['Users'] = df['Users'].rolling(14, win_type='triang', min_periods=1).sum()
    df['In-Game'] = df['In-Game'].rolling(14, win_type='triang', min_periods=1).sum()
    if plot:
        steam_processing_plot(df)


def steam_processing_plot(df):
    """!@brief Plots the results from the steam processing.

    @param df The data frame to use for plotting.
    """
    steam_df = df.melt('Date', value_vars=['Users', 'In-Game'],  var_name='cols', value_name='vals')

    g = sns.lineplot(x="Date", y="vals", hue='cols', data=steam_df)
    g.set_xticks(np.arange(0, len(df['Users']), 300))
    g.plot()
    plt.show()


def twitch_processing(df, plot):
    """!@brief Twitch processing function.

    @param df The data frame to process.
    @param plot Toggles the analysing plots. Plots can be time consuming to display. Switch off for better performance.
    """
    df['av_conc_viewers'].interpolate(method='polynomial', order=3, inplace=True)
    df['av_conc_channels'].interpolate(method='polynomial', order=3, inplace=True)
    df['time_watched'].interpolate(method='polynomial', order=3, inplace=True)
    df['active_streamers'].interpolate(method='polynomial', order=3, inplace=True)
    if plot:
        twitch_processing_plot(df)


def twitch_processing_plot(df):
    """!@brief Plots the results from the twitch processing.

    @param df The data frame to use for plotting.
    """
    fig, axes = plt.subplots(2, 2, sharex=False, sharey=False, figsize=(10, 10))

    twitch_df0 = df.melt('Date', value_vars=['av_conc_viewers'], var_name='cols', value_name='vals')
    twitch_df1 = df.melt('Date', value_vars=['av_conc_channels'], var_name='cols', value_name='vals')
    twitch_df2 = df.melt('Date', value_vars=['time_watched'], var_name='cols', value_name='vals')
    twitch_df3 = df.melt('Date', value_vars=['active_streamers'], var_name='cols', value_name='vals')

    g0 = sns.lineplot(x="Date", y="vals", hue='cols', data=twitch_df0, ax=axes[0, 0])
    g1 = sns.lineplot(x="Date", y="vals", hue='cols', data=twitch_df1, ax=axes[0, 1])
    g2 = sns.lineplot(x="Date", y="vals", hue='cols', data=twitch_df2, ax=axes[1, 0])
    g3 = sns.lineplot(x="Date", y="vals", hue='cols', data=twitch_df3, ax=axes[1, 1])
    g0.set_xticks(np.arange(0, len(df['av_conc_viewers']), 400))
    g1.set_xticks(np.arange(0, len(df['av_conc_channels']), 400))
    g2.set_xticks(np.arange(0, len(df['time_watched']), 400))
    g3.set_xticks(np.arange(0, len(df['active_streamers']), 400))
    g0.plot()
    g1.plot()
    g2.plot()
    g3.plot()
    plt.show()


def socialblade_processing(df, plot):
    """!@brief Socialblade processing function.

    @param df The data frame to process.
    @param plot Toggles the analysing plots. Plots can be time consuming to display. Switch off for better performance.
    """
    df['Weekly_average_change_views'] = df['Weekly_average_change_views'].interpolate(method='polynomial', order=3)
    df['Weekly_average_change_views'] = df['Weekly_average_change_views'].rolling(20, win_type='triang',
                                                                                  min_periods=1).sum()

    df['Weekly_average_views'] = df['Weekly_average_views'].interpolate(method='polynomial', order=3)
    mask = np.arange(0, len(df.Weekly_average_views))
    mask = mask < 905
    df.loc[mask, 'Weekly_average_views'] = np.where(df.loc[mask, 'Weekly_average_views'] > 3000000, 0,
                                                    df.loc[mask, 'Weekly_average_views'])
    df.loc[:, 'Weekly_average_views'] = np.where(df.loc[:, 'Weekly_average_views'] < 0, 0,
                                                 df.loc[:, 'Weekly_average_views'])
    df.loc[mask, 'Weekly_average_views'] = df.loc[mask, 'Weekly_average_views'].to_numpy() * np.linspace(1, 4, 905)

    df['Weekly_average_views'] = df['Weekly_average_views'].rolling(40, win_type='triang', min_periods=1).sum()
    if plot:
        socialblade_processing_plot(df)


def socialblade_processing_plot(df):
    """!@brief Plots the results from the socialblade processing.

    @param df The data frame to use for plotting.
    """
    fig, axes = plt.subplots(1, 2, sharex=False, sharey=False, figsize=(15, 15))
    socialblade_df0 = df.melt('Date', value_vars=['Weekly_average_change_views'], var_name='cols', value_name='vals')
    socialblade_df1 = df.melt('Date', value_vars=['Weekly_average_views'], var_name='cols', value_name='vals')
    g0 = sns.lineplot(x="Date", y="vals", hue='cols', data=socialblade_df0, ax=axes[0])
    g1 = sns.lineplot(x="Date", y="vals", hue='cols', data=socialblade_df1, ax=axes[1])

    g0.set_xticks(np.arange(0, len(df['Weekly_average_change_views']), 300))
    g0.set_title('Weekly_average_change_views')
    g1.set_xticks(np.arange(0, len(df['Weekly_average_views']), 300))
    g1.set_title('Weekly_average_views')

    g0.plot()
    g1.plot()
    plt.show()


def stock_processing(df, plot):
    """!@brief Stock processing function.

    @param df The data frame to process.
    @param plot Toggles the analysing plots. Plots can be time consuming to display. Switch off for better performance.
    """
    # Some keys were saved wrong, other stock codes contain mostly dirty information. Rename wrong named ones and delete
    # garbage information stocks determined by visual data inspection.
    df['PTR'] = df['PTR_x']
    df['EBAY'] = df['EBAY_x']
    for key in ['EBAY_x', 'EBAY_y', 'PTR_x', 'PTR_y', 'SHL', 'BAYN', 'JPHLF', 'SHE:002075', 'CON', 'CCCMF', 'INL']:
        if key in df.keys():
            df.drop(key, axis=1, inplace=True)

    # Interpolate stock data to avoid missing values due to NaN sums.
    for domain in sector_tuple_list:
        for code in domain.stock_code_list:
            if code in df.keys():
                df[code].interpolate(inplace=True)
        df[domain.df_column_name] = sum([(df[stock] - df[stock].mean()) / df[stock].std() for stock in
                                         domain.stock_code_list if stock in df.keys()]) / len(domain.stock_code_list)
        df[domain.df_column_name].replace(min(df[domain.df_column_name]), np.nan, inplace=True)
        df[domain.df_column_name].interpolate(method='polynomial', order=3, inplace=True)
    if plot:
        stock_processing_plot(df)


def stock_processing_plot(df):
    """!@brief Plots the results from the stock processing.

    @param df The data frame to use for plotting.
    """
    med_df = df.melt('Date', value_vars=['stock_med'], var_name='cols', value_name='vals')
    bank_df = df.melt('Date', value_vars=['stock_bank'], var_name='cols', value_name='vals')
    energy_df = df.melt('Date', value_vars=['stock_energy'], var_name='cols', value_name='vals')
    oil_df = df.melt('Date', value_vars=['stock_oil'], var_name='cols', value_name='vals')
    steel_df = df.melt('Date', value_vars=['stock_steel'], var_name='cols', value_name='vals')
    automotive_df = df.melt('Date', value_vars=['stock_automotive'], var_name='cols', value_name='vals')
    telecom_df = df.melt('Date', value_vars=['stock_telecom'], var_name='cols', value_name='vals')
    tech_df = df.melt('Date', value_vars=['stock_tech'], var_name='cols', value_name='vals')

    fig, axes = plt.subplots(4, 2, sharex=False, sharey=False, figsize=(15, 15))
    g0 = sns.lineplot(x="Date", y="vals", hue='cols', data=med_df, ax=axes[0, 0])
    g1 = sns.lineplot(x="Date", y="vals", hue='cols', data=bank_df, ax=axes[0, 1])
    g2 = sns.lineplot(x="Date", y="vals", hue='cols', data=energy_df, ax=axes[1, 0])
    g3 = sns.lineplot(x="Date", y="vals", hue='cols', data=oil_df, ax=axes[1, 1])
    g4 = sns.lineplot(x="Date", y="vals", hue='cols', data=steel_df, ax=axes[2, 0])
    g5 = sns.lineplot(x="Date", y="vals", hue='cols', data=automotive_df, ax=axes[2, 1])
    g6 = sns.lineplot(x="Date", y="vals", hue='cols', data=telecom_df, ax=axes[3, 0])
    g7 = sns.lineplot(x="Date", y="vals", hue='cols', data=tech_df, ax=axes[3, 1])

    g0.set_xticks(np.arange(0, 801, 200))
    g0.set_title('Average medical stock performance')
    g1.set_xticks(np.arange(0, 801, 200))
    g1.set_title('Average finance stock performance')
    g2.set_xticks(np.arange(0, 801, 200))
    g2.set_title('Average energy stock performance')
    g3.set_xticks(np.arange(0, 801, 200))
    g3.set_title('Average oil stock performance')
    g4.set_xticks(np.arange(0, 801, 200))
    g4.set_title('Average steel stock performance')
    g5.set_xticks(np.arange(0, 801, 200))
    g5.set_title('Average automotive stock performance')
    g6.set_xticks(np.arange(0, 801, 200))
    g6.set_title('Average telecom stock performance')
    g7.set_xticks(np.arange(0, 801, 200))
    g7.set_title('Average tech stock performance')

    g0.plot()
    g1.plot()
    g2.plot()
    g3.plot()
    g4.plot()
    g5.plot()
    g6.plot()
    g7.plot()

    fig.tight_layout()
    plt.show()


def index_processing(df, plot):
    """!@brief Stock index processing function.

    @param df The data frame to process.
    @param plot Toggles the analysing plots. Plots can be time consuming to display. Switch off for better performance.
    """
    for code in index_codes:
        df[code] = (df[code] - df[code].mean()) / df[code].std()
    if plot:
        index_processing_plot(df)


def index_processing_plot(df):
    """!@brief Plots the results from the stock index processing.

    @param df The data frame to use for plotting.
    """
    dax_df = df.melt('Date', value_vars=['DAX'], var_name='cols', value_name='vals')
    ndaq_df = df.melt('Date', value_vars=['NDAQ'], var_name='cols', value_name='vals')

    fig, axes = plt.subplots(1, 2, sharex=False, sharey=False, figsize=(15, 4))
    g0 = sns.lineplot(x="Date", y="vals", hue='cols', data=dax_df, ax=axes[0])
    g1 = sns.lineplot(x="Date", y="vals", hue='cols', data=ndaq_df, ax=axes[1])

    g0.set_xticks(np.arange(0, 801, 200))
    g0.set_title('DAX performance')
    g1.set_xticks(np.arange(0, 801, 200))
    g1.set_title('NDAQ performance')

    g0.plot()
    g1.plot()

    fig.tight_layout()
    plt.show()


def clean_df(df, verbose=False):
    """!@brief Dataframe cleaning function.

    Removes unnecessary columns and messy keys. Also unifies the naming scheme.

    @param df The data frame to process.
    @param verbose Toggles verbose output over the terminal.
    """
    for domain in sector_tuple_list:
        for code in domain.stock_code_list:
            if code in df.keys():
                df.drop(code, axis=1, inplace=True)

    for code in index_codes:
        if code in df.keys():
            df.drop(code, axis=1, inplace=True)

    messy_key_list = ['TDXP', 'INDU', 'NKY']
    for key in messy_key_list:
        if key in df.keys():
            df.drop(key, axis=1, inplace=True)

    # Unify naming scheme.
    df.rename(columns={'deaths': 'corona_deaths', 'confirmed': 'corona_confirmed', 'recovered': 'corona_recovered',
                       'active': 'corona_active', 'new_recovered': 'corona_new_recovered',
                       'new_deaths': 'corona_new_deaths',
                       'bitrate': 'ix_bitrate', 'Weekly_average_change_views': 'youtube_viewchange',
                       'Weekly_average_views': 'youtube_views', 'Users': 'steam_users', 'In-Game': 'steam_ingame',
                       'av_conc_viewers': 'twitch_views', 'av_conc_channels': 'twitch_channels',
                       'time_watched': 'twitch_viewtime',
                       'active_streamers': 'twitch_streams', 'PS': 'ps_users'}, inplace=True)
    if verbose:
        df.info()


def scale_split_df(df, end_index):
    """!@brief Data frame split and scaling.

    Scales the data with a fitted standard scaler from pre Corona times. Splits the data sets into two sets, one for pre
    Corona, one for during Corona.

    @param df The data frame to process.
    @param end_index Index of the 01.01.2020 in the data set.
    """
    # Rearrange column order to make scaling easy.
    cols = df.columns.tolist()
    cols = cols[8:26] + cols[1:7] + [cols[0]]
    df = df[cols]

    pre_corona_df = df.truncate(after=end_index)
    corona_df = df.truncate(before=end_index)

    scaler = StandardScaler()
    ct = ColumnTransformer([('scaler', scaler, np.arange(0, 24))], remainder='passthrough')
    scaled_pre_corona_data = ct.fit_transform(pre_corona_df)
    # Only transform, do not fit with corona data.
    scaled_corona_data = ct.transform(corona_df)

    scaled_pre_corona_df = pd.DataFrame(columns=pre_corona_df.columns, data=scaled_pre_corona_data.copy())
    scaled_corona_df = pd.DataFrame(columns=corona_df.columns, data=scaled_corona_data.copy())

    for key in corona_df.keys():
        if not key == 'Date':
            scaled_pre_corona_df[key] = pd.to_numeric(scaled_pre_corona_df[key], downcast="float")
            scaled_corona_df[key] = pd.to_numeric(scaled_corona_df[key], downcast="float")
    return pre_corona_df, corona_df, scaler


def save_df(scaled_pre_corona_df, scaled_corona_df, scaler):
    """!@brief Saves the data frames as well as the scaler.

    @param scaled_pre_corona_df The pre Corona data frame.
    @param scaled_corona_df The during Corona data frame.
    @param scaler The fitted scaler for the data sets.
    """
    root = Path().absolute().parent.parent

    scaled_pre_corona_df_path = root.joinpath('res', 'pipeline', 'scaled_pre_corona_df.csv')
    scaled_corona_df_path = root.joinpath('res', 'pipeline', 'scaled_corona_df.csv')

    scaled_pre_corona_df.to_csv(scaled_pre_corona_df_path)
    scaled_corona_df.to_csv(scaled_corona_df_path)

    # Save the scaler.
    joblib.dump(scaler, root.joinpath('res', 'pipeline', 'scaler.save'))
    print('Data sets saved.')


if __name__ == '__main__':
    pipeline(verbose=True, plot=False)
