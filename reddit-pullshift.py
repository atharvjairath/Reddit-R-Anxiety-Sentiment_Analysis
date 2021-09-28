import pandas as pd
import requests
import json
import datetime
import csv


def get_pushshift_data(after, before, sub):
    url = 'https://api.pushshift.io/reddit/search/submission/?&after='+str(after)+'&before='+str(before)+'&subreddit='+str(sub)+'&sort=asc&sort_type=created_utc'
    print(url)
    r = requests.get(url)
    data = json.loads(r.text, strict=False)
    return data['data']


def collect_subData(subm):
    subData = list() #list to store data points
    title = subm['title']
    url = subm['url']
    try:
        flair = subm['link_flair_text']
    except KeyError:
        flair = "NaN"
    try:
        # returns the body of the posts
        body = subm['selftext']
    except KeyError:
        body = ''
    author = subm['author']
    subId = subm['id']
    score = subm['score']
    created = datetime.datetime.fromtimestamp(subm['created_utc']) #1520561700.0
    numComms = subm['num_comments']
    permalink = subm['permalink']

    subData.append((subId,title,body,url,author,score,created,numComms,permalink,flair))
    subStats[subId] = subData


"""
    Uploads the data stored in 'subStats' into a CSV file for further
    data processing.
"""
def update_subFile():
    upload_count = 0
    location = "subreddit_data_uncleaned/"
    print("input filename of submission file, please add .csv")
    filename = input()
    file = location + filename
    with open(file, 'w', newline='', encoding='utf-8') as file:
        a = csv.writer(file, delimiter=',')
        headers = ["Post ID","Title","Body","Url","Author","Score","Publish Date","Total No. of Comments","Permalink","Flair"]
        a.writerow(headers)
        for sub in subStats:
            a.writerow(subStats[sub][0])
            upload_count+=1

        print(str(upload_count) + " submissions have been uploaded into a csv file")

#global dictionary to hold 'subData'
subStats = {}
#tracks no. of submissions
subCount = 0
#Subreddit name to scrape
sub='Anxiety'
# Unix timestamp 
# before to after
before = "1632846000"
after = "1625069971"
# Current time : 28/09/2021 : 1632846000
# 3 months before : 30/06/2021 : 1625069971
data = get_pushshift_data(after, before, sub)

while len(data) > 0:
    for submission in data:
        collect_subData(submission)
        subCount+=1
    print(len(data))
    print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
    after = data[-1]['created_utc']
    data = get_pushshift_data(after, before, sub)

print(len(data))

update_subFile()