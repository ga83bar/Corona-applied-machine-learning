"""everythin related to preprocessing - might be extended to a whole package if required"""
import joblib
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

from interface import PreprocessDataInterface   # pylint: disable=import-error


class CoronaPreprocessor(PreprocessDataInterface):
    '''
    CoronaPreprocessor (CP) preprocesses the corona data.
    We preprocess the data using pca to reduce the dimension.
    This class implements the PreprocessDataInterface!
    '''

    def __init__(self, scale_algo=1):
        '''
        Initialize CoronaPreprocessor (CP):
        @param saving_path : Path where the processed data should be stored.
        @param scale_algo : Selected scaling algo according to :
            PCA = 1
            STANDART_SCALING = 2
            Z_SCALING = 3
            Can also be set with set_scalinging_algorithm(algo)
        '''
        super(CoronaPreprocessor, self).__init__('covid', scale_algo)  # add also this!!
        self.cols_to_scale = ['deaths', 'confirmed', 'recovered', 'active',
                              'new_confirmed', 'new_recovered', 'new_deaths']

    def _pca(self, data, componenets=3):
        '''Abstract method. Implement PCA'''
        self.plot_singular_values(data, colums_to_drop=['Date'])
        data = pca(data, components=componenets, cols_to_scale=self.cols_to_scale)
        joblib.dump(data[0], self._path_to_scaler)
        return data[1]

    def _standart_scaling(self, data):
        '''Abstract method. Implement standart scaling'''
        data = standart_scale(data, cols_to_scale=self.cols_to_scale)
        joblib.dump(data[0], self._path_to_scaler)
        return data[1]

    def _min_max_scaling(self, data):
        '''Abstract method. Implement z scaling'''
        data = min_max_scale(data, cols_to_scale=self.cols_to_scale)
        joblib.dump(data[0], self._path_to_scaler)
        return data[1]


class PlaystationPreprocessing(PreprocessDataInterface):
    '''
    TODO
    '''
    def __init__(self, scale_algo=2):
        '''
        Initialize CoronaPreprocessor (CP):
        @param saving_path : Path where the processed data should be stored.
        @param scale_algo : Selected scaling algo according to :
            PCA                 = 1
            STANDART_SCALING    = 2
            Z_SCALING           = 3
            Can also be set with set_scalinging_algorithm(algo)
        '''
        super(PlaystationPreprocessing, self).__init__('playstation', scale_algo)
        self.cols_to_scale = ['PS3', 'PS4', 'Vita']

    def _pca(self, data, componenets=3):
        '''Abstract method. Implement PCA'''
        raise Exception('No PCA for PS data available!!')

    def _standart_scaling(self, data):
        '''Abstract method. Implement standart scaling'''
        data = standart_scale(data, cols_to_scale=self.cols_to_scale)
        joblib.dump(data[0], self._path_to_scaler)
        return data[1]

    def _min_max_scaling(self, data):
        '''Abstract method. Implement z scaling'''
        data = min_max_scale(data, cols_to_scale=self.cols_to_scale)
        joblib.dump(data[0], self._path_to_scaler)
        return data[1]


class SteamPreprocessing(PreprocessDataInterface):
    '''
    TODO
    '''
    def __init__(self, scale_algo=2):
        '''
        Initialize CoronaPreprocessor (CP):
        @param saving_path : Path where the processed data should be stored.
        @param scale_algo : Selected scaling algo according to :
            PCA                 = 1
            STANDART_SCALING    = 2
            Z_SCALING           = 3
            Can also be set with set_scalinging_algorithm(algo)
        '''
        super(SteamPreprocessing, self).__init__('steam', scale_algo)
        self.cols_to_scale = ['Users', 'In-Game']

    def _pca(self, data, componenets=3):
        '''Abstract method. Implement PCA'''
        raise Exception('No PCA for steam data available!!')

    def _standart_scaling(self, data):
        '''Abstract method. Implement standart scaling'''
        data = standart_scale(data, cols_to_scale=self.cols_to_scale)
        joblib.dump(data[0], self._path_to_scaler)
        return data[1]

    def _min_max_scaling(self, data):
        '''Abstract method. Implement z scaling'''
        data = min_max_scale(data, cols_to_scale=self.cols_to_scale)
        joblib.dump(data[0], self._path_to_scaler)
        return data[1]


class IXPreprocessor(PreprocessDataInterface):
    '''
    TODO MAX AARON:
    (1) TODOs implementieren
    --> Info in den methoden (scaling..) ist data der frame der im ix/processed folder liegt

    (2) Bitte alle .csv files in processed in ein file mergen --> pandas.merge oder irgenwie so
    --> !!!!! IM PROCESSED FOLDER DARF NUR EIN .csv LIEGEN !!!!!!

    (3) Stellt sicher das das datum richtige convertiert ist z.B.
    --> frame['Date] = pd.to_datetime(frame['Date], utc=True) (utc ist wichtig!!)

    (4) Name soll 'Date' bleiben, dann ist das überall einheitlich
    '''

    def __init__(self, scale_algo=2):  # TODO MAX & AARON set standart scaling algo
        '''
        Initialize CoronaPreprocessor (CP):
        @param saving_path : Path where the processed data should be stored.
        @param scale_algo : Selected scaling algo according to :
            PCA                 = 1
            STANDART_SCALING    = 2
            Z_SCALING           = 3
            Can also be set with set_scalinging_algorithm(algo)
        '''
        super(IXPreprocessor, self).__init__('ix', scale_algo)
        print('Inittialized IX preprocessor')

    def _pca(self, data, componenets=3):
        '''Abstract method. Implement PCA'''
        # TODO MAX & AARON return processed dataframe
        print('Not implemented.')

    def _standart_scaling(self, data):
        '''Abstract method. Implement standart scaling'''
        # TODO MAX & AARON return processed dataframe
        print('Not implemented.')

    def _min_max_scaling(self, data):
        '''Abstract method. Implement z scaling'''
        # TODO MAX & AARON return processed dataframe
        print('Not implemented.')


class DEIXPreprocessor(PreprocessDataInterface):
    '''
    TODO FELIX:
    (1) TODOs implementieren
    --> Info in den methoden (scaling..) ist data der frame der im de-cix/processed folder liegt

    (2) Bitte alle .csv files in processed in ein file mergen --> pandas.merge oder irgenwie so
    --> !!!!! IM PROCESSED FOLDER DARF NUR EIN .csv LIEGEN !!!!!!

    (3) Stell sicher das das datum richtige convertiert ist z.B.
    --> frame['Date] = pd.to_datetime(frame['Date], utc=True) (utc ist wichtig!!)
    --> Date attribut soll 'Date' heißen !!!!!!!!!

    (4) Name soll 'Date' bleiben, dann ist das überall einheitlich
    '''

    def __init__(self, scale_algo=2):  # TODO Felix set standart scaling algo
        '''
        Initialize CoronaPreprocessor (CP):
        @param saving_path : Path where the processed data should be stored.
        @param scale_algo : Selected scaling algo according to :
            PCA                 = 1
            STANDART_SCALING    = 2
            Z_SCALING           = 3
            Can also be set with set_scalinging_algorithm(algo)
        '''
        super(DEIXPreprocessor, self).__init__('ix', scale_algo)
        print('Inittialized IX preprocessor')

    def _pca(self, data, componenets=3):
        '''Abstract method. Implement PCA'''
        # TODO Felix return processed dataframe
        print('Not implemented.')

    def _standart_scaling(self, data):
        '''Abstract method. Implement standart scaling'''
        # TODO Felix return processed dataframe
        print('Not implemented.')

    def _min_max_scaling(self, data):
        '''Abstract method. Implement z scaling'''
        # TODO Felix return processed dataframe
        print('Not implemented.')


# ##################################################
# ###########       St functions         ###########
# ##################################################

def standart_scale(data, cols_to_scale=None):
    '''
    Standart function standart scaler. If you want you can simply use this inside
    your _standart_scaling method. But you have to clean the data first (No date..)
    '''
    scaler = StandardScaler()

    if cols_to_scale is None:
        data[data.columns] = scaler.fit_transform(data[data.columns])

    else:
        data[cols_to_scale] = scaler.fit_transform(data[cols_to_scale])
    return [scaler, data]


def min_max_scale(data, cols_to_scale=None):
    '''
    Standart function min_max_scaler. If you want you can simply use this inside
    your _min_max_scaling method. But you have to clean the data first (No date..)
    '''
    scaler = MinMaxScaler()

    if cols_to_scale is None:
        data[data.columns] = scaler.fit_transform(data[data.columns])

    else:
        data[cols_to_scale] = scaler.fit_transform(data[cols_to_scale])
    return [scaler, data]


def pca(data, components, cols_to_scale=None):
    '''!
    Do a PCA with the data. May it would be good if you first ran the
    singular value plot function to determine the number of componenets
    @param data : raw data
    @param components : number of principal components
    @param colls_to_scale : the collumns you want to scale as list. If none we take all.

    @return list containing the scaler so we can save it and the processed data
    '''
    # TODO standart scaling and PCA + add Date
    scaler = PCA(n_components=components)
    # cols = data.columns
    if cols_to_scale is None:
        data = scaler.fit_transform(data[data.columns])

    else:
        data = scaler.fit_transform(data[cols_to_scale])
    return [scaler, data]


def tests():
    '''
    INFO:
    If you use this interface itmakes your live easier (I hope so).

    For your class:
    call in your __init__ method the parent constructor according to the covidPreprocessor
    super('YOUR_class_name',self).__init__('folder_name', scaling_algo (1,2,3 see interface))

    After that the data is loaded from this folder ....

    You just have to implement the 3 methods
    (1) _min_max_scaling(self, data)
    (2) _standart_scaling(self, data)
    (3) _pca(self, data, componenets=3)

    for 1 + 2 you can also use the predefined standarts  e.g.
    def _min_max_scaling(....):
        return min_max_scale(data) BUT YOU HAVE TO CLEAN THE DATA FIRST (NO DATE ..)
    '''
    # add your classes in this style
    co_p = CoronaPreprocessor()
    st_p = SteamPreprocessing()

    frame_list = []

    col_list = [co_p, st_p]
    for col in col_list:
        frame_list.append(col.process())


if __name__ == '__main__':
    tests()
