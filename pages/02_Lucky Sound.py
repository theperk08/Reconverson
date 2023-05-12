import streamlit as st
import pandas as pd
import random 
import time
import sqlite3

curl = 'https://open.spotify.com/track/'
heart = 'img/heart.png'
check = 'https://i.ibb.co/thyXK5c/check.png'

if "select_genre" in st.session_state:
    del(st.session_state.select_genre)
if "select_music" in st.session_state:
    del(st.session_state.select_music)


# INIT FONCTION 
def create_playlist_db(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS playlist
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       track_id TEXT NOT NULL,
                       more TEXT NOT NULL)''')
    conn.commit()
    return conn

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

def add_track_to_playlist(conn, track_id, more=''):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO playlist (track_id, more) VALUES (?,?)", (track_id,more))
    conn.commit()

def is_like(conn, track_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM playlist WHERE track_id=?", (track_id,))
    rows = cursor.fetchall()
    if len(rows) == 0:
        return False
    else:
        return True

def get_sound_urls(id):
    track_info = df.loc[df['track_id'] == id, 'son_url']
    if type(track_info.iloc[0]) == str:
        st.audio(track_info.iloc[0])
     
db_conn = create_playlist_db("list.bdd")
add_logo()
# Chargement du dataframe
df = pd.read_csv('df_img.csv')
df_sound = pd.read_csv('df_sound.csv')

st.header('Lucky SoundTrack')
st.subheader('Découvre tes artistes grâce au hasard')

if "fortune" in st.session_state:
    ii = st.session_state.fortune
    col1, col2, col3 = st.columns([2, 4, 4])
    # Initialisation du composant empty
    with col1:
        if st.button("Reprendre"):
            del(st.session_state.fortune)
            st.experimental_rerun()
    with col2:
        st.image(ii)
    with col3:
        st.header(df[df['image_url'] == ii]['track_name'].iloc[0])
        st.subheader(df[df['image_url'] == ii]['genre'].iloc[0])
        url = curl+df[df['image_url'] == ii]['track_id'].iloc[0]
        html_code = f'<a href="{url}">Ecouter sur spotify</a>'
        st.markdown(html_code, unsafe_allow_html=True)
        ###############################################
        get_sound_urls(df[df['image_url'] == ii]['track_id'].iloc[0])
        if is_like(db_conn, df[df['image_url'] == ii]['track_id'].iloc[0]):
                st.image(heart, width=15)    
        else:
            m = st.markdown("""
                    <style>
                    div.stButton > button:first-child {
                        background: #E02800;
                        border: none;
                        color: white;
                        font-size: 9px;
                        padding: 2px 5px;
                    }
                    div.stButton > button:first-child:hover{
                        border:none;
                        background: #901A00;
                    }
                    </style>""", unsafe_allow_html=True)

            if st.button("like"):
                add_track_to_playlist(db_conn, df[df['image_url'] == ii]['track_id'].iloc[0])
                st.write(f"""<img src="{check}" width="15px"> """, unsafe_allow_html=True)
    
else:
    col1, col2, col3 = st.columns([1, 3, 1])
    # Initialisation du composant empty
    with col1:
        stop_button = st.button("Arrêter")
    with col2:
        text_output = st.empty()

    # Boucle infinie pour faire défiler les valeurs de la colonne 'image_url'
    while True:
        for image_url in df['image_url']:
            if stop_button:
                # Si le bouton "Arrêter" est cliqué, on sort de la boucle infinie
                break
            text_output.image(image_url, width=400)  # affichage de l'image dans l'empty
            st.session_state.fortune = image_url
            time.sleep(0.01)
        if stop_button:
            # Si le bouton "Arrêter" est cliqué, on sort de la boucle infinie
            break
        df = pd.read_csv('df_img.csv')  # rechargement du dataframe pour recommencer à la première ligne












