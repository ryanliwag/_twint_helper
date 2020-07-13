import twint 
import datetime
import time
from argparse import ArgumentParser
from pathlib import Path

def write_log(text, file):
    f = open(file, 'a')           # 'a' will append to an existing file if it exists
    f.write("{}\n".format(text))  # write the text to the logfile and move to next line
    return

def main(search, start_date, increment, nb_increment, logfile):
    twitter_module(search, start_date, int(increment), int(nb_increment), logfile)


def twint_scrapper(word_search, since, limit):
    c = twint.Config()
    #Configuration 
    c.Search = word_search
    c.Since = since
    c.Until = limit
    c.Show_hashtags = True
    c.Store_csv = True
    c.Lang= "en"
    #c.Verified=True
    c.proxy_host="tor"
    c.Output = word_search + ".csv"

    #start_searching 
    twint.run.Search(c)


def twitter_module(search_words, start_date, increments, nb_days, logfile):    
    #start_date = datetime.datetime.now() - datetime.timedelta(days=(97))
    start_date = datetime.datetime.strptime(start_date, "%d-%m-%Y")
    final_date = start_date - datetime.timedelta(days=(increments))
    for j in range(nb_days):
        connected = False
        while not connected: 
            try:
                write_log(search_words + " <"+ str(datetime.datetime.now()) +">"+"scraping time range since " + final_date.strftime("%Y-%m-%d") + " until " + start_date.strftime("%Y-%m-%d"), logfile)  # Write the specified text to the logfile
                print("since " + final_date.strftime("%Y-%m-%d") + " until " + start_date.strftime("%Y-%m-%d"))
                twint_scrapper(search_words, final_date.strftime("%Y-%m-%d"), start_date.strftime("%Y-%m-%d"))
                write_log("<"+  str(datetime.datetime.now()) +">"+"Done " + final_date.strftime("%Y-%m-%d") + " until " + start_date.strftime("%Y-%m-%d"), logfile)  # Write the specified text to the logfile

                connected = True
            except:
                print("failed")
                write_log("<"+  str(datetime.datetime.now())+">"+" failed time period scrape" + final_date.strftime("%Y-%m-%d") + " until " + start_date.strftime("%Y-%m-%d"), logfile)  # Write the specified text to the logfile
                write_log("retrying in 10 seconds", logfile)  # Write the specified text to the logfile
                print("retrying in 10 seconds")
                time.sleep(10)
                pass
        start_date = final_date
        final_date = final_date - datetime.timedelta(days=increments)


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("-s", "--search_word", help="phrase or word to search", required=True)
    parser.add_argument("-dt", "--starting_date", help="Input starting date. Format:dd-mm-yyyy Example: 07-03-2018")
    parser.add_argument("-i", "--day_increment", help="number of days to search before saving", required=True)
    parser.add_argument("-d", "--nb_increment", help="number of times to repeat increments", required=True)
    args = parser.parse_args()

    logfile = r"logfile.log"  # name of my log file
    my_file = Path(logfile)
    if my_file.is_file():
        print("logfile exists")
    else:
        open(logfile,"w+")

    write_log("Starting New Session...", logfile)
    main(args.search_word, args.starting_date, args.day_increment, args.nb_increment, logfile)
