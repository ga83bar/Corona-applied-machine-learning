import os
from pytrends.request import TrendReq

dir_path = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()
def get_keywords(keywords_file):
    kw_file = open(keywords_file)
    keywords = []
    for line in kw_file:
        # "#" are supposed to be comments on txt file
        if line[0] != '#':
            keywords.append(line[:-1])
    print(keywords)
    return keywords

def get_interest_over_time(kw_list):
    
    #kw_lists = list(divide_chunks(kw_list, 5))
    pytrend = TrendReq()
    # Interest by Region
    counter = 1
    
    for kw in kw_list:
        pytrend.build_payload(kw_list=[kw])
        trends_df = pytrend.interest_over_time()
        trends_df.drop("isPartial", 1, inplace=True)
        trends_df.to_csv("{}/Data/{}.csv".format(dir_path, kw))
        counter += 1

def divide_chunks(list, size):
    # looping till length l
    for keyword in range(0, len(list), size):
        yield list[keyword + size]
def get_data():
    kw_list = get_keywords("{}/keywords.txt".format(dir_path))
    get_interest_over_time(kw_list)

get_data()