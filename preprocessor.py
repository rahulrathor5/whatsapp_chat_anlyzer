import re
import pandas as pd
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    message=re.split(pattern,data)[1:]

    dates=re.findall(pattern,data)

    df=pd.DataFrame({'user_message':message,'message_date':dates})

    #convert the datetime_Format
    df['message_date']=pd.to_datetime(df['message_date'],format="%m/%d/%y, %H:%M - ")

    df.rename(columns={'message_date':'date'},inplace=True)

    #seperate users and message
    user=[]
    message=[]
    for i in df['user_message']:
     entry=re.split(r'^(.*?):\s(.*)$',i)
     if entry[1:]: #username
        user.append(entry[1])
        message.append(entry[2])
     else:
      user.append('group_notification')
      message.append(entry[0])
    df['user']=user
    df['message']=message
    df.drop(columns=['user_message'],inplace=True)

    df['year']=df['date'].dt.year

    df['month']=df['date'].dt.month_name()

    df['day']=df['date'].dt.day

    df['day_name']=df['date'].dt.day_name()

    df['only_date']=df['date'].dt.date

    df['hour']=df['date'].dt.hour

    df['month_num']=df['date'].dt.month

    df['minute']=df['date'].dt.minute

    period=[]
    for hour in df[['day_name','hour']]['hour']:
        if hour==23:
            period.append(str(hour)+"-"+str('00'))
        elif hour==0:
            period.append(str('00')+"-"+str(hour+1))
        else:
            period.append(str(hour)+"-"+str(hour+1))
    
    df['period']=period

    return df



