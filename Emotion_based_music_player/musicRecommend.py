import streamlit as st
import pandas as pd
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data


page_bg_img = '''
<style>
body {
background-image: url("https://img.freepik.com/free-vector/geometric-pattern-purple-technology-background-with-circles_53876-116189.jpg?w=900&t=st=1657804363~exp=1657804963~hmac=edd6a194a097e573bb3af81db9b0da534eea9c538d10152ba566ca61446add8f");
background-size: cover;
}
</style>
'''



def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://img.freepik.com/free-vector/geometric-pattern-purple-technology-background-with-circles_53876-116189.jpg?w=900&t=st=1657804363~exp=1657804963~hmac=edd6a194a097e573bb3af81db9b0da534eea9c538d10152ba566ca61446add8f");
             background-size: 200 200
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
set_bg_hack_url()



client_id = 'client_id'
client_secret = 'secret_id'
client_credentials_manager = SpotifyClientCredentials(client_id='6d57f32dcf244e299783a02fe4ce7997', client_secret='69d7c23fb9ac4df88ec2a80ec2ed1cb5')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API
# sp = authorisation.authorize()

dp=pd.read_csv('Genre_dataset2.csv')
artist_data=pd.read_csv('Genre_dataset2.csv')

artist_list=[]
for i in artist_data['artist_name']:
    if i not in artist_list:
        artist_list.append(i)


genre_list=[]
for i in dp['genre']:
    if i not in genre_list:
        genre_list.append(i)
 
mode_list=['genre','artist']


def recommend(genr):
    ll=[]
    pp=[]
    cc=[]
    c=0
    for i in dp['genre']:
        if i==genr:
            pp.append(dp['song_name'][c])
            cc.append(dp['audio'][c])
            ll.append(dp['img'][c])
        c=c+1
    return pp,cc,ll



def Fetch_name_audio_img(artist):
    ll=[]
    pp=[]
    cc=[]
    c=0
    count=0
    for i in artist_data['artist_name']:
        if i==artist:
            count=count+1
            ll.append(artist_data['song_name'][c])
            pp.append(artist_data['audio'][c])
            cc.append(artist_data['img'][c])

        # if count==6:
        #     return ll,pp,cc
        c=c+1
    return ll,pp,cc





st.header('Music Player')
selected_mode = st.sidebar.selectbox(
    "Select the mode",mode_list
)

st.markdown(page_bg_img, unsafe_allow_html=True)

if selected_mode=='genre':
    selected_music = st.selectbox(
    "Select a genre of music for Playing",genre_list
    )
    
    if st.button('Display Music'):
        song_name,audio,img= recommend(selected_music)
        size=len(song_name)
        size=int(size/3)
        col1, col2, col3 = st.columns(3)
        for i in range(0,size):
            with col1:
                st.image(img[i*3+0])
                st.text(song_name[i*3+0])
                st.audio(audio[i*3+0])
            with col2:
                st.image(img[i*3+1])
                st.text(song_name[i*3+1])
                st.audio(audio[i*3+1])

            with col3:
                st.image(img[i*3+2])
                st.text(song_name[i*3+2])
                st.audio(audio[i*3+2])



elif selected_mode=='artist':
    selected_artist = st.selectbox(
    "Select a artist",artist_list
    )
    
    if st.button('Display Music'):
        song_name,audio,img=Fetch_name_audio_img(selected_artist)
        size=len(song_name)
        # st.write(size)
        col=0
        if size > 3:
            col=int(size/3)
        for i in range(0,col):    
            col1, col2, col3 = st.columns(3)
            # col4, col5, col6 = st.columns(3)
            with col1:
                st.image(img[i*3+0])
                st.text(song_name[i*3+0])
                st.audio(audio[i*3+0])

            with col2:
                st.image(img[i*3+1])
                st.text(song_name[i*3+1])
                st.audio(audio[i*3+1])

            with col3:
                st.image(img[i*3+2])
                st.text(song_name[i*3+2])
                st.audio(audio[i*3+2])

            