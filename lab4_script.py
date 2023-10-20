#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import praw
import time  
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from datetime import datetime
from pytz import timezone 
import hashlib
import mysql.connector

USER_AGENT = 'Lab4API by /u/kickdoorkick75'
CLIENT_ID = '3yBWXZ5kyqMBH8IGzL8V0g'
SECRET_KEY = 'pJ1OixUkvUcB9ggdh5AtgjRptb8soA'

reddit = praw.Reddit(user_agent=USER_AGENT,
                     client_id=CLIENT_ID, client_secret=SECRET_KEY)

def fetcher(subreddit_name, num_posts):
    
    subreddit,post_data,post_remained,max_posts_per_request,after = reddit.subreddit(subreddit_name),[],num_posts, 1000, None
 

    while post_remained > 0:

        posts_to_fetch = min(post_remained, max_posts_per_request)
        

        posts = subreddit.top(limit=posts_to_fetch, params={"after": after})

        for post in posts:
            
            body = post.selftext if post.selftext else post.url

            post_data.append({
                'title': post.title,
                'body': body,
                'Id_Author' : post.id,
                'created_utc': post.created_utc,
                'keywords': '',  
                'topics': ''    
            })


        post_remained -= posts_to_fetch


        after = post.fullname


        time.sleep(3)  
        
    return post_data

if __name__ == "__main__":
    subreddit_name = 'tech'
    
    inp=int(input('Number of post to fetch: '))
     
    data_fetched = fetcher(subreddit_name, inp)

# Function to convert the time to PST

def time_process(time):

    utc_datetime = datetime.utcfromtimestamp(time)


    target_time_zone = 'US/Pacific'
    from_zone = utc_datetime.tzinfo
    to_zone = timezone(target_time_zone)


    localized_datetime = utc_datetime.astimezone(to_zone)


    formatted_datetime = localized_datetime.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_datetime



for item in data_fetched:
    time = item['created_utc']
    returned_time = time_process(time)

    item['created_utc'] = returned_time
    


nltk.download('punkt',quiet=True)
nltk.download('averaged_perceptron_tagger',quiet=True)




# Function to extract keywords and topics from a given title
def extract_keywords_and_topics(title):

    words = word_tokenize(title)

    words_tagged = pos_tag(words)
    

    keywords = []
    topics = []
    

    keyword_tags = ['NN', 'JJ', 'JJR', 'JJS', 'NNS', 'NNP', 'NNPS']
    
    for word, pos in words_tagged:

        if pos in keyword_tags:
            keywords.append(word)
        else:
            topics.append(word)
    

    keyword_str = ' '.join(keywords)
    topic_str = ' '.join(topics)
    
    return keyword_str, topic_str


for item in data_fetched:
    title = item['title']
    keywords, topics = extract_keywords_and_topics(title)
    

    item['keywords'] = keywords
    item['topics'] = topics
    



def author_masking(author_id):

    mask = "Data_Wranglers"


    combined_data = author_id + mask


    masked = hashlib.sha256(combined_data.encode()).hexdigest()

    return masked

for item in data_fetched:
    author = item['Id_Author']
    masked_name = author_masking(author)
    
    item['Id_Author_masked'] = masked_name

    
    
## Now, below we are writing the code to add this data to sql server


# Connecting to the MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='reddit_data'
)

cursor = conn.cursor()


for post in data_fetched:
    sql = "INSERT INTO reddit_posts (title, body, author, created_utc, keywords, topics) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (post['title'], post['body'], post['Id_Author'], post['created_utc'], post['keywords'], post['topics'])
    cursor.execute(sql, values)

conn.commit()
conn.close()

