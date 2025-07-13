import re
import pandas as pd
import streamlit as st
import preprocessor,helper
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('chat_analyzer')


# File uploader
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode('utf_8')
    df=preprocessor.preprocess(data)
#     st.dataframe(df)


    #fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'overall')


    selected_user=st.sidebar.selectbox("show anlysis wrt",user_list)
    
    if (st.sidebar.button('show analysis')):
         
         # stats area 

         num_message,word,media_count,link_len=helper.fetch_stats(selected_user,df)
        
         col1,col2,col3,col4=st.columns(4)

         with col1:
              st.header('total messages')
              st.title(num_message)

         with col2:
              st.header('total words')
              st.title(word)
         with col3:
              st.header('media shared')
              st.title(media_count)
         with col4:
              st.header('link shared')
              st.title(link_len)
         #monthly_timeline

         timeline=helper.monthly_timeline(selected_user,df)
         fig,ax=plt.subplots()
         st.title('montly timeline')
         ax.plot(timeline['time'],timeline['message'],color='green')
         plt.xticks(rotation='vertical')
         st.pyplot(fig)

         #daily_timeline

         new_timeline=helper.daily_timeline(selected_user,df)
         
         fig,ax=plt.subplots()
     #     plt.figure(figsize=(18,10))
         st.title('daily timeline')
         ax.plot(new_timeline['only_date'],new_timeline['message'],color='orange')
         plt.xticks(rotation='vertical')
         st.pyplot(fig)

         #activity map

         st.title('activity_map')
         col1,col2=st.columns(2)
         with col1:
             st.header('most busy day')
             busy_day=helper.week_activity(selected_user,df)
             fig,ax=plt.subplots()
             ax.bar(busy_day.index,busy_day.values,color='green')
             plt.xticks(rotation='vertical')
             st.pyplot(fig)
         with col2:
             st.header('most busy month')
             busy_month=helper.month_activity(selected_user,df)
             fig,ax=plt.subplots()
             ax.bar(busy_month.index,busy_month.values,color='orange')
             plt.xticks(rotation='vertical')
             st.pyplot(fig)

          #daily_Activity
         st.title('acitvity_heatmap')

         activity_table=helper.most_activity_time(selected_user,df)
         fig,ax=plt.subplots()
         ax=sns.heatmap(activity_table)
         st.pyplot(fig)
         

         
         
          #find the most active user in group(group level)

         if selected_user=='overall':
            st.title('most active user')

            x=df['user'].value_counts().head()
            
            name=x.index

            count=x.values

            fig,ax=plt.subplots()

            col1,col2=st.columns(2)
            
            with col1:
                 ax.bar(name,count,color='yellow')
                 plt.xticks(rotation='vertical')
                 st.pyplot(fig)
            with col2:
              x=helper.active_user(df)
              st.dataframe(x)
        
        
        # word cloud
         st.title('word_cloud')
         df_wc=helper.create_wordcloud(selected_user,df)
         fig,ax=plt.subplots()
         ax.imshow(df_wc)
         st.pyplot(fig)
         
         # most common used word

         most_common_df=helper.most_common_word(selected_user,df)

         fig,ax=plt.subplots()
         ax.barh(most_common_df[0],most_common_df[1])
         plt.xticks(rotation='vertical')
         st.title('most_commom_words')
         st.pyplot(fig)
         # st.dataframe(most_common_df)


         # emoji analysis

         emoji_df=helper.find_emoji(selected_user,df)
         st.title('emoji analysis')

         col1,col2=st.columns(2)
         with col1:
             st.dataframe(emoji_df)
         with col2:
             fig,ax=plt.subplots()
             ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
             st.pyplot(fig)
         





            

     


