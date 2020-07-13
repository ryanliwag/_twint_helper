import twint 
import datetime
import time
from argparse import ArgumentParser
from pathlib import Path

import twint

config  = twint.Config()
config.Search
config.Username


import threading
import asyncio

# def launch_query(c):
#     asyncio.set_event_loop(asyncio.new_event_loop())
#     twint.run.Search(c)

# max_queries=3 #numero de consultas simultaneas
# twint_array=[]
# for i in range(max_queries):
#     twint_array.append(twint.Config())
#     twint_array[i].Search = "#tesla"
#     twint_array[i].Timedelta =2
#     twint_array[i].Count = True
#     twint_array[i].Limit = "20"

# if (i==0):
# twint_array[i].search_name ="test_ca"
# twint_array[i].Lang = "ca"
# elif i==1:
# twint_array[i].search_name ="test_es"
# twint_array[i].Lang = "es"
# elif i==2:
# twint_array[i].search_name ="test_en"
# twint_array[i].Lang = "en"
# print(i)
# print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
# hilo1 = threading.Thread(target=launch_query, args=(twint_array[0],))
# print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
# hilo2 = threading.Thread(target=launch_query, args=(twint_array[1],))
# print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
# hilo3 = threading.Thread(target=launch_query, args=(twint_array[2],))
# hilo1.start()
# hilo2.start()

# #scrap followers

# "Burger King #Burger #King"

# import twint


# "apple OR banana OR orange"

# " OR ".join(keywordList)
    # # start_date = datetime.datetime.strptime(start_date, "%d-%m-%Y")
    # # final_date = start_date - datetime.timedelta(days=(increments))
    # for j in range(nb_days):
    #     connected = False
    #     while not connected: 
    #         try:
    #             write_log(search_words + " <"+ str(datetime.datetime.now()) +">"+"scraping time range since " + final_date.strftime("%Y-%m-%d") + " until " + start_date.strftime("%Y-%m-%d"), logfile)  # Write the specified text to the logfile
    #             print("since " + final_date.strftime("%Y-%m-%d") + " until " + start_date.strftime("%Y-%m-%d"))
    #             twint_scrapper(search_words, final_date.strftime("%Y-%m-%d"), start_date.strftime("%Y-%m-%d"))

class twint_scraper():
    def __init__(self, resume_file):

        self.config = twint.Config()
        self.resume = resume_file + ".txt"

    def scrape_hashtags(self, hashtags, since, until):

        self.config.Search = hashtags
        self.config.Since = since
        self.config.Until = until
        self.config.Show_hashtags = True


        #min likes, min retweets, native tweets, popular tweets, filter on meida, images, videos

        self.config.Store_csv = True
        self.config.proxy_host = "tor"
        self.config.Filter_retweets = True #remove retweets
        
        self.config.Min_delay = 2
        self.config.Max_delay = 10

        self.config.Output = hashtags+".csv"

        twint.run.Search(self.config)


import pandas as pd



def launch_query(c):
    asyncio.set_event_loop(asyncio.new_event_loop())
    twint.run.Search(c)

def config_setup(usernames):
    for user in usernames:
        print(user)
        c = twint.Config()
        c.Username = user
        c.Store_csv = True
        c.Output = 'files/' + user + '.csv'
        twint.run.Following(c)

if __name__ == "__main__":

    # scraper = twint_scraper("hija_ako_id")
    # scraper.scrape_hashtags("#hijaako", since="2020-06-01", until="2020-07-12")

    g = pd.read_csv("hijaako.csv")
    usernames = g["username"].unique()
    usernames = usernames[:300]
    username_split = []
    threads = 3
    print(len(usernames))
    val = int(len(usernames) / threads)
    start = 0;
    end = val
    for i in range(threads-1):
        print(start, end)
        username_split.append(usernames[start:end])
        start += val
        end += val

    username_split.append(usernames[start:])



    for i in username_split:
        print(len(i))

    thread_list = []

    for thr in range(threads):
        thread = threading.Thread(target=config_setup, args=(username_split[thr],),)
        thread_list.append(thread)
        thread_list[thr].start()

    for thread in thread_list:
        thread.join()

    


    # parser = ArgumentParser()
    # parser.add_argument("-s", "--search_word", help="phrase or word to search", required=True)
    # parser.add_argument("-dt", "--starting_date", help="Input starting date. Format:dd-mm-yyyy Example: 07-03-2018")
    # parser.add_argument("-i", "--day_increment", help="number of days to search before saving", required=True)
    # parser.add_argument("-d", "--nb_increment", help="number of times to repeat increments", required=True)
    # args = parser.parse_args()

    # logfile = r"logfile.log"  # name of my log file
    # my_file = Path(logfile)
    # if my_file.is_file():
    #     print("logfile exists")
    # else:
    #     open(logfile,"w+")

    # write_log("Starting New Session...", logfile)
    # main(args.search_word, args.starting_date, args.day_increment, args.nb_increment, logfile)
