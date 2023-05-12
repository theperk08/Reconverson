import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import json

delete_img = 'https://i.ibb.co/tXhVw3k/delete.png'


if "select_genre" in st.session_state:
    del(st.session_state.select_genre)
if "select_music" in st.session_state:
        del(st.session_state.select_music)

conn = sqlite3.connect('list.bdd')

resultats = []

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
def get_sound_urls(id):
    track_info = df_cover.loc[df_cover['track_id'] == id, 'son_url']
    if type(track_info.iloc[0]) == str:
        st.audio(track_info.iloc[0])
add_logo()

# Afficher la playlist

c = conn.cursor()
c.execute('SELECT * FROM playlist')
playlist = c.fetchall()

df_bd = pd.DataFrame(playlist, columns=['id', 'track_id', 'more'])

df = pd.read_csv('DataFrame_Musique.csv')
df_cover = pd.read_csv('df_img.csv')
df_sound = pd.read_csv('df_sound.csv')

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
        get_sound_urls(ligne['track_id'])
    with col3:
        st.subheader(ligne['track_name'])
    with col4:
        if st.button('unlike', key=ligne['track_id']):
            delete_track_from_playlist(conn, ligne['track_id'])
            st.write(f"""<img src="{delete_img}" width="15px"> """, unsafe_allow_html=True)

# Convertir la ligne en un dictionnaire sérialisable en JSON
    dict_ligne = {}
    ligne = ligne.astype(str)
    for col in ligne.index:
        # Convertir les valeurs Pandas en types de données Python nativement sérialisables en JSON
        if pd.isna(ligne[col]):
            dict_ligne[col] = None
        elif isinstance(ligne[col], (pd.Timestamp, pd._libs.tslibs.nattype.NaTType)):
            dict_ligne[col] = str(ligne[col])
        elif isinstance(ligne[col], pd.Categorical):
            dict_ligne[col] = str(ligne[col].item())
        else:
            dict_ligne[col] = ligne[col]

    # Ajouter le dictionnaire de la ligne dans la liste des résultats
    resultats.append(dict_ligne)

# Convertir la liste des dictionnaires en un objet JSON
json_str = json.dumps(resultats)

# Écrire l'objet JSON dans un fichier
with open("resultats.json", "w") as f:
    f.write(json_str)

with st.expander("Afficher le contenu du JSON"):
    st.write(json.loads(json_str))

conn.close()