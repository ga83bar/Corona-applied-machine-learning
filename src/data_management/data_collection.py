"""collects data"""

class DataCollection():
    '''This class is responsible for collecting raw data from div databases or API`s'''

    def __init__(self):
        self.get_raw_data()

    def get_raw_data(self):
        '''Most important method of cls DataCollection returns the raw data as pandas frame'''
        self.get_raw_covid_data

    def parse_data_from_online_source(self):
        '''Most important method of cls DataCollection returns the raw data as pandas frame'''
        raise NotImplementedError

    def get_raw_covid_data(self, start_date, end_date):
        '''
        this function returns a the world wide, daily covid data:
        NewConfirmed, TotalConfirmed, NewDeaths, TotalDeaths, NewRecovered
        and TotalRecovered
        '''
        # FIXME
        countries = ['south-africa', 'switzerland', 'germany']

        # TODO convert date time object to this kind of format
        date_start = '2019-04-01T00:00:00Z'
        date_end = '2020-05-01T00:00:00Z'

        # create a list containing date time objects from to
        split_start = date_start.split('T')
        start = datetime.datetime.strptime(split_start[0], "%Y-%m-%d")
        split_end = date_end.split('T')
        end = datetime.datetime.strptime(split_end[0], "%Y-%m-%d")

        # select one of the requests:
        # this is too much data to handle with my pc =(
        # get_request = "https://api.covid19api.com/all"
        get_request = 'https://api.covid19api.com/world?from={}&to={}'.format(
            date_start, date_end)
        # this request returns the data for a specific country
        # get_request = []
        # for single_country in countries:
        #     get_request.append('https://api.covid19api.com/live/country/{}/status/confirmed/date/{}T13:13:30Z'.format(single_country, split_start[0]))
        # df = self.covid_request(get_request[2])

    def get_date_list(self, start_date, end_date):
        '''
        Generates a list of dates containing all dates from start_date to end_date
        '''
        date_list = [start_date + datetime.timedelta(days=x) for x in range(0, (end_date - start_date).days)]
        return date_list

    def covid_request(self, get_request, plot=True):
        '''
        Returns the data from the request as pandas frame.
        May we should drop the data we do not need??
        '''
        covid_request = request.get(get_request)
        # process the data if it was a valid request
        if covid_request.status_code == 200:
            # print(request.text)
            df = pd.read_json(covid_request.text)
            print(df.head())
        else:
            print('REQUEST STATUS : {}'.format(covid_request.status_code))
            raise Exception('NO valid request!!')

        self.handle_result(df, bool_plot=plot)
        return df

    def handle_result(self, dataframe, save_frame=False, bool_plot=True):
        '''
        Here we define what we want to do with the data
        '''
        if save_frame:
            dataframe.to_pickle("./dummy.pkl")

        if bool_plot:
            dataframe.plot(kind='line', title='Some title', x='Date', y=['Confirmed', 'Deaths', 'Active'])

            plt.show()


data_collector = DataCollection()
