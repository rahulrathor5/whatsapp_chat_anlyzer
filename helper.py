import emoji.unicode_codes
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
import seaborn as sns
from urlextract import URLExtract
extract=URLExtract()

f=open('stop_hinglish.txt','r')
stop_words=f.read()

def fetch_stats(selected_user,df):

    if selected_user!='overall':
        df=df[df['user']==selected_user]


    # 1.number of message
    num_message=df.shape[0]

    # 2.number of word
    word=[]
    for message in df['message']:
        word.extend(message.split())

    
    # 3. fetch the media count 
    media_count=df[df['message']=='<Media omitted>'].shape[0]

   # 4. fetch the number of link
    link=[]
    for i in df['message']:
        link.extend(extract.find_urls(i))



        
    return num_message,len(word),media_count,len(link)

def active_user(df):

    df=round(df['user'].value_counts()/df.shape[0]*100,2).reset_index().rename(
        columns={'index':'name','user':'percent'}
    )

    return df

def create_wordcloud(selected_user,df):
    if selected_user!='overall':
        df=df[df['user']==selected_user]

     #remove the group notification
    temp=df[df['user']!='group_notification']
    #remove the media
    temp=temp[temp['message']!='<Media omitted>']

    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc=wc.generate((temp['message']).str.cat(sep=" "))
    return df_wc

def most_common_word(selected_user,df):
    if selected_user!='overall':
        df=df[df['user']==selected_user]
    #remove the group notification
    temp=df[df['user']!='group_notification']
    #remove the media
    temp=temp[temp['message']!='<Media omitted>']
    
    #remove the stopwords
    words=[]

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    

    new_df=pd.DataFrame(Counter(words).most_common(30))
    return new_df
    

#finding the emojis

def find_emoji(selected_user,df):

    if selected_user!='overall':
        df=df[df['user']==selected_user]

    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

      
def monthly_timeline(selected_user,df):
     if selected_user!='overall':
        df=df[df['user']==selected_user]
     timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
     time=[]
     for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+'-'+str(timeline['year'][i]))
     timeline['time']=time
     return timeline

def daily_timeline(selected_user,df):
    if selected_user!='overall':
        df=df[df['user']==selected_user]
    timeline=df.groupby('only_date').count()['message'].reset_index()
    return timeline

def week_activity(selected_user,df):
    if selected_user!='overall':
        df=df[df['user']==selected_user]
    return df['day_name'].value_counts()

def month_activity(selected_user,df):
    if selected_user!='overall':
        df=df[df['user']==selected_user]
    return df['month'].value_counts()

def most_activity_time(selected_user,df):
    if selected_user!='overall':
        df=df[df['user']==selected_user]
    acitivity_table=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return acitivity_table

