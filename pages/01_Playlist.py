import streamlit as st
import sqlite3
import pandas as pd
import numpy as np

if "select_genre" in st.session_state:
    del(st.session_state.select_genre)
if "select_music" in st.session_state:
        del(st.session_state.select_music)

conn = sqlite3.connect('list.bdd')


# INIT FONCTION 
def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://i.ibb.co/Fs4gnZX/radio.png);
                background-repeat: no-repeat;
                background-position: center;
                padding-top: 120px;
                background-position: 30px 20px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
def ms_to_minsec(ms):
    seconds = int(ms / 1000)
    minutes = int(seconds / 60)
    seconds -= minutes * 60
    return f"{minutes:02}:{seconds:02}"
def delete_track_from_playlist(conn, track_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM playlist WHERE track_id = ?", (track_id,))
    conn.commit()

add_logo()

# Afficher la playlist

c = conn.cursor()
c.execute('SELECT * FROM playlist')
playlist = c.fetchall()

df_bd = pd.DataFrame(playlist, columns=['id', 'track_id', 'more'])

df = pd.read_csv('DataFrame_Musique.csv')
df_cover = pd.read_csv('df_img.csv')

#### CRE LA LIST LIKE ID
likeId = []
for index, row in df_bd.iterrows():
    if row['track_id']:
        likeId.append(row['track_id'])


if len(likeId) == 0:
    st.header('La playlist est vide')


sum_ms = 0
for i in range(len(likeId)):
    ligne = df_cover.loc[df_cover['track_id'] == likeId[i]].iloc[0]
    sum_ms += ligne['duration_ms']

tt = ms_to_minsec(sum_ms)
aa = [tt, ' min']
ttt = ' '.join(aa)

colA, colB = st.columns(2)
with colA:
    st.subheader('Durée totale de la playlist ')
with colB:
    st.subheader(ttt)



#st.write(likeId)
for i in range(len(likeId)):
    ligne = df_cover.loc[df_cover['track_id'] == likeId[i]].iloc[0]
    col1, col2, col3, col4 = st.columns([1,1,4,1])
    with col1:
        st.image(ligne['image_url'])     
    with col2:
        st.subheader(ms_to_minsec(ligne['duration_ms']))
    with col3:
        st.subheader(ligne['track_name'])
    with col4:
        if st.button('unlike', key=ligne['track_id']):
            delete_track_from_playlist(conn, ligne['track_id'])
            st.write('Effacé')


conn.close()