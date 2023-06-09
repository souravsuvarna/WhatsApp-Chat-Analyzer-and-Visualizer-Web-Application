import streamlit as st
import preprocessor,helper
import pandas as pd
import plotly.express as px
import altair as alt
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import emoji
import sys
from PIL import Image,ImageFilter

st.set_page_config(page_title="WhatsApp Chat Analyzer", page_icon=":zap:",layout="wide",initial_sidebar_state='auto')

## Title and headers

img = Image.open('logomain.png')

filtered_img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150))

filtered_img.save('filtered_image.png')


img = Image.open('filtered_image.png')

st.image(img,width=175)

st.markdown("""<h1 style='text-align: center; color: white; font-family:'silver-forte', sans-serif;'>WhatsApp Chat Analyzer <sup style='font-size: 0.5em; vertical-align: super; color: rgba(144, 141, 143, 0.9);'>beta</sup></h1><style>
        h1 sup {
            font-size: 0.7em;
            vertical-align: super;
            color: rgba(144, 141, 143, 0.9);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #E9E8E8; font-family:'alata', sans-serif;'>Get insights into your chats. No chat data is sent to a server! All code runs locally in your browser. </p>", unsafe_allow_html=True)

hyperlink="https://drive.google.com/file/d/1CEHHmU3kuGegCMWzgIx142RZwGEraiJp/view?usp=sharing"
text="How it Works?"

##File Uploader

uploaded_file = st.file_uploader("Choose a file")
st.markdown(f"[{text}]({hyperlink})") ##document link will be here
if uploaded_file is not None:
    # To read file as bytes:
    
    bytes_data = uploaded_file.getvalue()
    try:
    
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)
    
        
        
    
    
    
    
        #Creating user_list to have unique users in drop down menu
        user_list = df['user'].unique().tolist()
        
        #sorting usernames in user_list
        user_list.sort()
        
        #Insert Overall for group analysis
        user_list.insert(0,"Overall Group")
        
        #Creating drop down of user_list
        
        selected_user = st.selectbox("Select Analysis of",user_list)
        
        
        
        #Creating Show Button
        
        if st.button("Show Analysis"):
            
            #calling helper.py for counting num(msg) & num(words) & num(media) & num(links) and many more sections
            
            #-->1.Begining of First Section
            
            num_messages ,num_words, num_media , num_links = helper.fetch_stats(selected_user,df)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:  #Displaying Tot(no of messages)
                
                st.header("Total Messages ")
                st.title(num_messages)
                
            with col2:  #Displaying Tot(no of words)
                st.header("Total Words")
                st.title(num_words)
        
            with col3: #Displaying Tot(media)
                st.header("Media Shared")
                st.title(num_media)
            
            with col4:
                st.header("Link Shared")
                st.title(num_links)
    
    
            #Here we completed with first section
        
            st.write("       ") #For gap purpose
            st.write("       ")
            st.write("       ")
            

            #-->2.) Beginning of 2nd section to find overall activity of selected user
            
            #Activity over a time period
            
            st.title("Inclusive Activity of the "+selected_user)
            
            df5=helper.activity_over_time(selected_user,df)    #will have dataframe of particular date and num(msg) done on that day 

            #Drawing Line Chart
            fig = px.line(df5, x='Date', y='Message',color_discrete_sequence=["#ff97ff"],width=1250,height=500)

            fig.update_layout(xaxis=dict(
            fixedrange=True  # Disable zooming on x-axis
            ),
            yaxis=dict(
            fixedrange=True  # Disable zooming on y-axis
            )
            )
            
            st.write(fig)
                
                
            st.write("       ") #For gap purpose
            
            #----Section 2 Completed---
            
            
            
            #-->3.Beginning of 3rd section  "Top 10 Active Users" this section will be displayed only if selected_user="OVERALL GROUP"
            
            if selected_user=='Overall Group':
        
                #Top 5 users and percentage
                col1,col2= st.columns(2)
                
                with col1:
                    
                    st.title("Top 5 Active Members")
                    
                    #Calling function
                    
                    df2 = helper.top_active_users(df) #will have top 5 user dataframe  with name and tot(msg) column 
                    
                    #Drawing Graph
                    
                    fig=alt.Chart(df2).mark_bar(color='#83C9FF').encode(x=alt.X('User',sort=list(df2['User'])),y='Message').properties(height=500,width=550)
                    st.write(fig)
                    
                with col2:
                    #Pie Chart for % of messages done by users
                    
                    st.title("Percentage of Chats")
                    
                    df3 = helper.percentage(df) # will have a data frame of  2 columns i.e user and his percentage of messages
                    
                    #Drawing pie chart
                    
                    fig = px.pie(df3, values='Percentage', names='User', hole=.3, color_discrete_sequence=px.colors.sequential.RdBu)
                    
                    fig.update_layout(margin=dict(t=30, b=30, l=30, r=30)) #Resizing the chart
                    
                    st.write(fig)
                    
                st.write("       ") #gap Purpose
                st.write("       ")
                col3,col4 = st.columns(2)
                
                with col3:
                    st.title("Top 5 Late Night Users")
                    
                    df6 = helper.late_night(df) # will have dataframe of late night users
                    
                    fig = go.Figure(go.Bar(x=df6['Messages'],y=df6['User'],marker={'color': [1,2,3,4,5], 'colorscale': 'purpor'},orientation='h'))
                    
                    fig.update_layout(template="seaborn", xaxis_title='Messages', yaxis_title='User', width=600,height=525)

                    
                    st.write(fig)
                    
                with col4:
                    st.title("Top 5 Early Morning Users")
                    
                    df6 = helper.early_morning(df)  # will have dataframe of early morning users
                    
                    fig = go.Figure(go.Bar(x=df6['Messages'],y=df6['User'],marker={'color': [1,2,3,4,5], 'colorscale': 'tealgrn'},orientation='h'))
                    
                    fig.update_layout(template="seaborn", xaxis_title='Messages', yaxis_title='User', width=600,height=525)
                    
                    st.write(fig)
                
                st.write("       ") #gap purpose
                st.write("       ")
                col5,col6 = st.columns(2)
                
                with col5:
                    st.title("Most Emoji Shared Users")
                    
                    df7 = helper.emoji(df)  #will have dataframe of top 5 emoji shared users
                    
                    
                    fig = px.bar(df7, x='User', y='Emoji',color_discrete_sequence=px.colors.sequential.Plasma_r) 
                    
                    fig.update_layout(template="seaborn",width=550,height=500)
                    
                    st.write(fig)
                
                with col6:
                    st.title("Most Media Shared Users")
                    
                    df8 = helper.media(df)  #will have dataframe of top 5 media shared users
                    
                    fig = px.bar(df8, x='User', y='Media',color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                    
                    fig.update_layout(template="seaborn", width=550,height=500)
                    
                    st.write(fig)
                    
            #---- Section 3 Completed ---- 
            
        
        
        
            #---- Section 4 starts
            
            st.write("       ") #gap Purpose
            st.write("       ")
            
            st.title('Most Active Month of '+selected_user)
            
            dfmonth = helper.month_chart(selected_user,df)  #will have dataframe of monthly activity chart

            fig = px.bar(dfmonth, x='Month',y='Message',color_discrete_sequence=px.colors.sequential.Magenta)
                
            fig.update_layout(template="seaborn", width=1200,height=500)
                
            st.write(fig)
        
            #--- Section 4 ends 
        
        
        
            #----Section 5 begins
            
            st.write("       ")
            
            st.title("Most Active Hours of "+selected_user)
            
            dftime = helper.time_chart(df,selected_user)    #this will have hourly activity dataframe
            
            fig = px.bar(dftime,x='Hour',y='Message',color_discrete_sequence=px.colors.sequential.Tealgrn)
            
            fig.update_layout( xaxis = dict(tickmode = 'linear'),template="seaborn", width=1200,height=500)
                
            st.write(fig)     
            
            #--- Secion 5 ends ---
            
            
            
            #-----Section 6 starts----
        
            col9,col10=st.columns(2)
            st.write("       ") #gap Purpose
            st.write("       ")
            
            
            with col9:
                st.title("Most Active Week Days")
                
                dfweek = helper.day_chart(selected_user,df) #Will have dataframe of weekly active days
                
                fig = px.bar(dfweek, x='Day',y='Message',color_discrete_sequence=px.colors.sequential.Oryel_r)
                
                fig.update_layout(template="seaborn", width=600,height=500)
                
                st.write(fig)
                
            with col10:
                st.title("Most Shared Emojis")
                
            
                if selected_user != 'Overall Group':
                    df = df[df['user'] == selected_user] 
            
                emojis=[]
                for message in df['message']:
                    emojis.extend([c for c in message if emoji.emoji_list(c)])
                s=len(emojis)
                
                if s>0:
                    
                    df9 = pd.DataFrame(emojis)

                    df9.rename(columns={0:'Emoji'},inplace=True)

                    df9 = df9.value_counts().reset_index()
                    df9.rename(columns={0:'Sent'},inplace=True)
                    df9=df9.head(10)
                
                    fig = px.pie(df9, values='Sent', names='Emoji',hole=.3, color_discrete_sequence=px.colors.sequential.Sunset)
                    fig.update_layout(margin=dict(t=30, b=30, l=30, r=30))
                    st.write(fig)
                else:
                    st.caption("Seems like "+selected_user+" not sent any emojis ")
        
        #----Section 6 complete----
    
    
    
    
        #---- Section 7 starts , word cloud
            #gap Purpose
            st.write("       ")
            
            st.title("Word Cloud of "+selected_user) 
            st.write("       ")
            st.write("       ")
            wc = helper.create_wordcloud(selected_user,df)  #will have image
            if wc:
                plt.figure( figsize=(20,10), facecolor='k',edgecolor ='k') #size set
                
                plt.imshow(wc,interpolation = 'bilinear')  #show image
                plt.axis("off") #axis turn off , so no x& y axis will be in image
                plt.tight_layout(pad=0)
                plt.savefig('wordcloud.png', facecolor='k', bbox_inches='tight')    #enchancing quality
                
                st.pyplot(plt) #print image
            else:
                st.caption("Unable to Fetch the data due to least activity of "+selected_user)
            
        #--- Section 7 Ended--

    except Exception as e:
        st.write("Seems like you uploaded wrong file, Kindly Reload this page and upload correct one.")
        st.caption( "Refer "+ hyperlink+" for further information ")




# Credit Section
# Define the developer name and their GitHub and LinkedIn URLs
developer_name = "Sourav Suvarna"
github_url = "https://github.com/souravsuvarna"
linkedin_url = "https://www.linkedin.com/in/souravsuvarna/"

developer_name1= "Suhas BS"
github_url1 = "https://github.com/suhasbs2000"
linkedin_url1 = "https://www.linkedin.com/in/suhas-bs-80b508112"

# Create a row with the name and icons

st.title("")
st.markdown("<p style='text-align: center; color: #E9E8E8; font-family:'alata', sans-serif;'>Developed by </p>", unsafe_allow_html=True)

container = st.container()
container.markdown(f"<div style='display: flex; align-items: center; justify-content: center;'><p style='margin-right: 10px;'>{developer_name} <a href='{github_url}' target='_blank'><img style='margin-right: 10px; width:25px;height:25px; background-color: white; border-radius: 50%;' src='https://github.com/favicon.ico' alt='GitHub'></a> <a href='{linkedin_url}' target='_blank'><img style='width: 20px; height: 20px;' src='https://www.linkedin.com/favicon.ico' alt='LinkedIn'></a></p></div>", unsafe_allow_html=True)

       
container.markdown(f"<div style='display: flex; align-items: center; justify-content: center;'><p style='margin-right: 10px;'>{developer_name1} <a href='{github_url1}' target='_blank'><img style='margin-right: 10px;width:25px;height:25px;  background-color: white; border-radius: 50%;' src='https://github.com/favicon.ico' alt='GitHub'></a> <a href='{linkedin_url1}' target='_blank'><img style='width: 20px; height: 20px;' src='https://www.linkedin.com/favicon.ico' alt='LinkedIn'></a></p></div>", unsafe_allow_html=True)


st.title("")

# Contact Support


st.markdown("<h2 style='text-align: center; color: #E9E8E8; font-family:'alata', sans-serif;'>Feedback</h2>", unsafe_allow_html=True)


contact_form = """
<form action="https://formsubmit.co/feedback.wachatanalyzer@gmail.com" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required >
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here" ></textarea>
     <button type="submit">Send</button>
</form>
"""

st.markdown(contact_form, unsafe_allow_html=True)

# Use Local CSS File
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")

# Support Ends

st.caption('© 2023. All rights reserved.')