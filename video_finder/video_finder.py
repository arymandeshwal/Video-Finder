#!/usr/bin/env python
# coding: utf-8

# In[1]:


from apiclient.discovery import build
from datetime import datetime, timedelta
import pandas as pd


# In[2]:


api_key = "AIzaSyD121AwAdKYfbk0Z7Gc0XYF3FKxPzFu0J4"
youtube = build("youtube","v3",developerKey=api_key)


# In[3]:


def create_df(items):
    df = pd.DataFrame(columns = ["VIDEO NAME","VIDEO URL","VIDEO VIEWS","NUMBER OF SUBS","RATIO","VIDEO VALUE"])
    #print(len(df.index))
    for i in items:
        video_name,video_url,video_views,no_of_channel_subs,ratio,video_value = each_entry_for_df(i)
        df.loc[len(df.index)] = [video_name,video_url,video_views,no_of_channel_subs,ratio,video_value]
    
    return df


# In[4]:


def each_entry_for_df(item):
    video_name, video_id, channel_name, channel_id = get_video_name(item)
    #print(video_name, video_id, channel_name, channel_id)
    video_views = int(get_video_views(video_id))
    no_of_channel_subs = int(get_no_of_channel_subs(channel_id))
    video_url = get_video_url(video_id)
    #print(video_name,video_url)
    ratio = get_ratio(video_views,no_of_channel_subs)
    days_since_published = get_days_since_published(video_id)
    video_value = get_video_value(video_views,ratio,days_since_published)
    #print(video_value)
    return video_name,video_url,video_views,no_of_channel_subs,ratio,video_value


# In[5]:


def get_days_since_published(video_id):
    #print(video_id)
    date = youtube.videos().list(id=video_id,part="snippet").execute()
    date = date["items"][0]["snippet"]["publishedAt"]
    datetime_object = datetime.strptime(date,"%Y-%m-%dT%H:%M:%SZ")
    current = datetime.today()
    days_since_published = (current - datetime_object).days
    if days_since_published == 0:
        return 1
    else:
        return days_since_published


# In[6]:


def get_video_value(video_views,ratio,days_since_published):
    score = video_views*ratio
    score = score/days_since_published
    return score


# In[7]:


def get_ratio(video_views,no_of_channel_subs):
    if no_of_channel_subs == 0:
        return 0
    else:
        ratio =  video_views/no_of_channel_subs
        return min(ratio,5) # 5 is threshold, to avoid clickbaits and small channels


# In[8]:


def get_video_url(video_id):
    video_url = "https://www.youtube.com/watch?v=" + video_id
    return video_url


# In[9]:


def get_no_of_channel_subs(channel_id):
    stats = youtube.channels().list(id = channel_id,part="statistics").execute()
    if stats['items'][0]['statistics']['hiddenSubscriberCount']:
        return 1000000
    else:
        return stats["items"][0]["statistics"]["subscriberCount"]


# In[10]:


def get_video_views(video_id):
    stats = youtube.videos().list(id = video_id,part="statistics").execute()
    return stats["items"][0]["statistics"]["viewCount"]


# In[11]:


def get_video_name(item):
    return item["snippet"]["title"],item["id"]["videoId"],item["snippet"]["channelTitle"],item["snippet"]["channelId"]


# In[12]:


def get_list_of_videos(youtube):
    days_before = int(input("Videos in last _____ days.\t"))
    query = input("Enter your search query:\t")
    video_list_details = youtube.search().list(q = query,part="snippet",type="video",order='viewCount',publishedAfter=getting_date_time(days_before),maxResults=50).execute()
    return video_list_details['items']


# In[13]:


def getting_date_time(days_before):
    current_date = datetime.today() - timedelta(days_before)
    return current_date.strftime('%Y-%m-%dT%H:%M:%SZ')


# In[14]:


def clean_df(df):
    df = df.loc[df['VIDEO VIEWS'] >= 5000]
    df.sort_values(["VIDEO VALUE"], axis=0, 
                 ascending=False, inplace=True)
    return df.head(5)


# In[15]:


def main():
    youtube = build("youtube","v3",developerKey=api_key)
    video_list_details = get_list_of_videos(youtube)
    df = create_df(video_list_details)
    df = clean_df(df)
    return df["VIDEO URL"].tolist()


# In[16]:


#df


# In[ ]:




