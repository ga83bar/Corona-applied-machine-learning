import pandas as pd                        
from pytrends.request import TrendReq
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()
def get_keywords(keywords_file):
    a = open(keywords_file)
    keywords = []
    for line in a:
        # "#" are supposed to be comments on txt file
        if line[0] != '#':
            keywords.append(line[:-1])
    print(keywords)
    return keywords

def get_interest_over_time(kw_list):
    x = list(divide_chunks(kw_list, 5)) 
    pytrend = TrendReq()
    # Interest by Region
    counter = 1 
    for kw_list in x:
        pytrend.build_payload(kw_list = kw_list)
        df = pytrend.interest_over_time()
        
        df.drop("isPartial",1,inplace=True) 
        
        df.to_csv("{}/Data/{}.csv".format(dir_path,counter))
        counter+=1

def divide_chunks(list, n): 
    # looping till length l 
    for i in range(0, len(list), n):  
        yield list[i:i + n] 


kw_list = get_keywords("{}/keywords.txt".format(dir_path))
get_interest_over_time(kw_list)
