import pandas as pd
import re
import preprocessor
from wordcloud import WordCloud

from urlextract import URLExtract   #library to extract links from messages

extract = URLExtract()  #Creating object of URLExtract Class

#-->1.Function for 1st section
 
def fetch_stats(selected_user,df):
    
    if selected_user != 'Overall Group':
        
        df = df[df['user'] == selected_user]    #masking dataframe to have only selected_user data
        
    #if selected_user is "overall" then no changes in dataframe    
    
    #1.fetching no of messages
    num_messages = df.shape[0]
        
    #2.fetching number of words
        
    words = [] #createing a list for storing individual messages
        
    for message in df['message']:
        words.extend(message.split())   #spliting messages to words and extend the list
     
        
    #3.feching no of media sent
    
    media = df[df['message']=='<Media omitted>\n'].shape[0]
    
    
    #4.fetching no of links
    
    links = [] #list to store links
    for message in df['message']:
        links.extend(extract.find_urls(message))
        
    return num_messages,len(words),media,len(links)    #len return length of list(i.e) number of elements in the list

#-----   End of first section function -----




#-->2.Function for 2nd Section

#Activity overall time period

def activity_over_time(selected_user,df):
    
    if selected_user != 'Overall Group':
        
        df = df[df['user'] == selected_user]  
    
    df5=df.copy()   #considering another dataframe
    
    df5['month_num'] = df5['date'].dt.month #created  a column for concating month num to date
    
    df5.drop(columns={'date','user','message','hour','minute'},inplace=True)  #droping unnecassary columns  
    
    df5 = preprocessor.activity_over_period(df5) #calling function to retrun final dataframe
    
    return df5 #retruns dataframe 

#----   Section 2 Completd ---- 




#-->2.Function for 3rd Section

#1.) Top 5 active users

def top_active_users(df):
    
    x=df['user'].value_counts().head(5) #this will counts no of times a row of particular username from repeated in the data frame and return top 5 repeated rows
    
    df2 = x.reset_index().rename(columns={'index':'User','user':'Message'}) # Creating a data frame df2. Here reset_index() function will converts x to a dataframe, contains columns index and user respectively, So we renaming the columns here
    
    return df2


#2.)Percentage of chat contribution

def percentage(df): #Percentage chart
    
    y=(df['user'].value_counts()/df.shape[0])*100 #Return Percentages with index and users columns as default column names where index has username and user has percentage of respective users
    
    df3=y.reset_index().rename(columns = {'index':'User','user':'Percentage'})  # converting y to data frame and renaming the columns
                
    df3.Percentage=df3.Percentage.round(2) #Rounding floating points to 2 decimals of percentage column
                
    df4=df3 #copying dataframe df3 to df4 (its done bcs we will have only top 9 users data in pie chart and one data called 'others' in order to calculate 'others' we will have df4 then we append df4 with df3 )
                
    df3=df3.head(9) #will have top 9 users data rows
                
    df4.drop(columns=['User'],inplace=True) #dropping User column in df4 as its not need
                
    sum=df4.sum()-df4.iloc[0:9].sum()   #formula:- sum(percentage of others)=sum(all users percentages)-sum(top 9 users percentage)
                
    sum=sum.reset_index()   #converting sum to dataframe
                
    sum.drop(columns=['index'],inplace=True)    #as sum is list intially it will have a default column called index so we drop that column
                
    df3 = df3.append({'User' : 'Others','Percentage' : sum[0][0]} , ignore_index=True)  #we append sum data frame that will have percentage of others to existing top 9 data frame df3 so now df3 will have 10 records 
    
    return df3
 

#3.) Top 5 Late night Users

def late_night(df):
    df6=df.loc[(df['hour']>22) | (df['hour']<4)]
    df6=df6['user'].value_counts().head(5)
    df6=df6.reset_index()
    df6.rename(columns={'index':'User','user':'Messages'},inplace=True)
    return df6   


#4.) Top 5 Early morning users

def early_morning(df):
    df6=df.loc[(df['hour']>3) & (df['hour']<7)]
    df6=df6['user'].value_counts().head(5)
    df6=df6.reset_index()
    df6.rename(columns={'index':'User','user':'Messages'},inplace=True)
    return df6

#5.) Top 5 Emoji shared users

def emoji(df):
    df7=df.copy()
    df7.drop(columns={'date','year','month','day','hour','minute'},inplace=True)
    df7["Emoticons"]=df7["message"].apply(lambda x:re.findall(r'[\U0001f600-\U0001f650]', x))
    df7["Emoticons_count"]=df7["message"].apply(lambda x:len(re.findall(r'[\U0001f600-\U0001f650]', x)))
    emoji=df7.groupby(["user"])["Emoticons_count"].sum().sort_values(ascending=False)
    emoji=emoji.reset_index().head(5)
    emoji.rename(columns={'user':'User','Emoticons_count':'Emoji'},inplace=True)
    return emoji

#6.) Top 5 media shared users

def media(df):
    df8 = df[df['message']=='<Media omitted>\n']
    df8=df8['user'].value_counts().reset_index().head(5)
    df8.rename(columns={'index':'User','user':'Media'},inplace=True)
    return df8

#----   Section 3 Completd ----  

 
 
#--- Section 4 starts

def month_chart(selected_user,df):
    if selected_user != 'Overall Group':
        df = df[df['user'] == selected_user]
        
    dfmonth=df['month']
    dfmonth=dfmonth.reset_index()
    dfmonth.drop(columns={'index'},inplace=True)
    dfmonth=dfmonth['month'].value_counts()
    dfmonth=dfmonth.reset_index()
    dfmonth.rename(columns={'index':'month','month':0},inplace=True)
    m_order = ['January', 'February', 'March', 'April', 'May', 'June','July','August','September','October','November','December']
    dfmonth['month'] = pd.Categorical(dfmonth['month'], categories=m_order, ordered=True)
    dfmonth = dfmonth.sort_values('month')  #Sorting month accordng to month name
    dfmonth.rename(columns={'month':'Month',0:'Message'},inplace=True)
    return dfmonth

#-- Section 4 ends ---




# --- Section 5 begins

def time_chart(df,selected_user):
    if selected_user != 'Overall Group':
        df = df[df['user'] == selected_user]
    dftime = df['hour']
    dftime=dftime.reset_index()
    dftime=dftime['hour'].value_counts()
    dftime=dftime.reset_index()
    dftime.rename(columns={'index':'Hour','hour':'Message'},inplace=True)
    dftime=dftime.sort_values(by='Hour')
    return dftime   

# --Section 5 ends ---



#----   Section 6 starts ----

def day_chart(selected_user,df):
    if selected_user != 'Overall Group':
        df = df[df['user'] == selected_user] 
        
    df['dayname']=df['date'].dt.day_name()
    dfweek = df['dayname']
    dfweek=dfweek.reset_index()
    dfweek.drop(columns={'index'},inplace=True)
    dfweek=dfweek['dayname'].value_counts()
    dfweek=dfweek.reset_index()
    dfweek.rename(columns={'index':'dayname','dayname':0},inplace=True)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
    dfweek['dayname'] = pd.Categorical(dfweek['dayname'], categories=day_order, ordered=True)
    dfweek = dfweek.sort_values('dayname')  #Sorting days according to weekdays
    dfweek.rename(columns={'dayname':'Day',0:'Message'},inplace=True)
    return dfweek

#---    Section 6 ends --





#--- Word Cloud---

def create_wordcloud(selected_user,df):
    if selected_user != 'Overall Group':
        df = df[df['user'] == selected_user]    #Mask User
    df = df[df['message']!='<Media omitted>\n'] #Media ommited msg will be removed
    df = df[df['message']!='This message was deleted\n']     #Deleted unwanted message
    if len(df)>10:
        wc = WordCloud(width=1600, height=800)  #size of image
        df_wc = wc.generate(df['message'].str.cat(sep=" ")) #generates image
        
        return df_wc
    

#-- Word cloud closed ---