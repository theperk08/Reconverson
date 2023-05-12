import streamlit as st
import pandas as pd
from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import sqlite3
import math

from sklearn.neighbors import NearestNeighbors

#INIT PAGE
st.set_page_config(
    page_title="Wild School Radio - Reconver'son",
)

# DEFINE CONST
curl = 'https://open.spotify.com/track/'
heart = 'img/heart.png'
cover_false = 'https://i.ibb.co/ZWSPvxB/nf.png'
radio_ets = 'img/radio.png'
check = 'https://i.ibb.co/thyXK5c/check.png'
btn_music = []
btn_genre = []


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

def raccourcir_chaine(chaine, nb_caracteres_max=30):
    if len(chaine) <= nb_caracteres_max:
        return chaine
    else:
        raccourci = chaine[:nb_caracteres_max-3] + '...'
        return raccourci

def is_like(conn, track_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM playlist WHERE track_id=?", (track_id,))
    rows = cursor.fetchall()
    if len(rows) == 0:
        return False
    else:
        return True

def create_playlist_db(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS playlist
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       track_id TEXT NOT NULL,
                       more TEXT NOT NULL)''')
    conn.commit()
    return conn

def add_track_to_playlist(conn, track_id, more=''):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO playlist (track_id, more) VALUES (?,?)", (track_id,more))
    conn.commit()

def delete_track_from_playlist(conn, track_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM playlist WHERE track_id = ?", (track_id,))
    conn.commit()

def ms_to_minutes(millis):
    minutes = millis // 60000
    return minutes

def ms_to_min_sec(millis):
    minutes = millis // 60000
    seconds = (millis // 1000) % 60
    return f"{minutes:02d}:{seconds:02d}"

def is_square_image(file_path):
    # Vérifie si une image a un format carré 1:1
    img = Image.open(file_path)
    return img.size[0] == img.size[1]

def get_image_urls(id):
    img_series = df_cover.loc[df_cover['track_id'] == id, 'image_url']
    if type(img_series.iloc[0]) == str:
        return img_series.iloc[0]
    else:   
        return cover_false

def get_track_name(id):
    getname = df.loc[df['track_id'] == id, 'track_name']
    if type(getname.iloc[0]) == str:
        return getname.iloc[0]
    else:
        return 'Titre introuvable' 

def get_sound_urls(id):
    track_info = df_cover.loc[df_cover['track_id'] == id, 'son_url']
    if type(track_info.iloc[0]) == str:
        st.audio(track_info.iloc[0])
    
def row_5(list_):

    col1, col2, col3, col4 = st.columns([2,5,2,5])
    if len(list_)>0:
        with col1:
            img_urls = get_image_urls(list_[0])
            html_code = f'<a href="{curl+list_[0]}"><img width="80px" src="{img_urls}"></a>'
            st.markdown(html_code, unsafe_allow_html=True)
        with col2:
            st.write("""<span style="font-size:15px; font-weight:bold">""",raccourcir_chaine(get_track_name(list_[0])),"""<span>""", unsafe_allow_html=True)
        
            collike, colson = st.columns([2,8])
            with collike:
                if is_like(db_conn, list_[0]):
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

                    if st.button("like", key=list_[0]):
                        add_track_to_playlist(db_conn, list_[0])
                        st.write(f"""<img src="{check}" width="15px"> """, unsafe_allow_html=True)
                with colson:
                    get_sound_urls(list_[0])

            if len(list_)>1:
                with col3:
                    img_urls = get_image_urls(list_[1])
                    html_code = f'<a href="{curl+list_[1]}"><img width="80px" src="{img_urls}"></a>'
                    st.markdown(html_code, unsafe_allow_html=True)

                with col4:
                    st.write("""<span style="font-size:15px; font-weight:bold">""",raccourcir_chaine(get_track_name(list_[1])),"""<span>""", unsafe_allow_html=True)
                    collike, colson = st.columns([2,8])
                    with collike:
                        if is_like(db_conn, list_[1]):
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

                            if st.button("like", key=list_[1]):
                                add_track_to_playlist(db_conn, list_[1])
                                st.write(f"""<img src="{check}" width="15px"> """, unsafe_allow_html=True)
                    with colson:
                        get_sound_urls(list_[1])
                    
def row_top(list_):

    col1, col2, col3 = st.columns(3)
    if len(list_)>0:
        with col1:
            img_urls = get_image_urls(list_[0])
            html_code = f'<a href="{curl+list_[0]}"><img width="250px" src="{img_urls}"></a>'
            # Affichage du code HTML
            st.markdown(html_code, unsafe_allow_html=True)
            get_sound_urls(list_[0])
            if is_like(db_conn, list_[0]):
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

                if st.button("like", key=list_[0]):
                    add_track_to_playlist(db_conn, list_[0])
                    st.write(f"""<img src="{check}" width="15px"> """, unsafe_allow_html=True)
        if len(list_)>1:
            with col2:
                img_urls = get_image_urls(list_[1])
                html_code = f'<a href="{curl+list_[1]}"><img width="250px" src="{img_urls}"></a>'
                # Affichage du code HTML
                st.markdown(html_code, unsafe_allow_html=True)      
                get_sound_urls(list_[1])
                if is_like(db_conn, list_[1]):
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

                    if st.button("like", key=list_[1]):
                        add_track_to_playlist(db_conn, list_[1])
                        st.write(f"""<img src="{check}" width="15px"> """, unsafe_allow_html=True)
                
            if len(list_)>2:
                with col3:
                    img_urls = get_image_urls(list_[2])
                    html_code = f'<a href="{curl+list_[2]}"><img width="250px" src="{img_urls}"></a>'
                    # Affichage du code HTML
                    st.markdown(html_code, unsafe_allow_html=True)
                    get_sound_urls(list_[2])
                    if is_like(db_conn, list_[2]):
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

                        if st.button("like", key=list_[2]):
                            add_track_to_playlist(db_conn, list_[2])
                            st.write(f"""<img src="{check}" width="15px"> """, unsafe_allow_html=True)

# END FONCITON $
add_logo()
# INIT DB et BDD
db_conn = create_playlist_db("list.bdd")
df = pd.read_csv('DataFrame_Musique.csv')
df_cover = pd.read_csv('df_img.csv')
df_sound = pd.read_csv('df_sound.csv')

#st.write(df_cover)

# DEFINITION DES VAR
genres_uniques = df["genre"].explode().unique()
titre_musiques = df["track_name"].explode().unique()
duree_max  = ms_to_minutes(math.ceil(df["duration_ms"].max()))
duree_min  = ms_to_minutes(math.floor(df["duration_ms"].min()))

# FILTRES
reco_by = st.sidebar.radio("", ['Filtres', 'Select Music'])

if reco_by == 'Filtres':

    if "select_music" in st.session_state:
        del(st.session_state.select_music)

    f_genre = st.sidebar.multiselect('GENRES',genres_uniques, max_selections=3)
    f_duree = st.sidebar.slider('DUREE',duree_min, duree_max, (duree_min, duree_max))
    f_bpm = st.sidebar.slider('BPM',30, 300, (100, 200)) # bpm == tempo
    f_r = st.sidebar.slider('Nombre de resultat', 15, 100)
    # slide one point sur popularity
    btn_genre = st.sidebar.button('RECHERCHE')

if reco_by == 'Select Music':
    if "select_genre" in st.session_state:
        del(st.session_state.select_genre)

    val_music = st.sidebar.selectbox('Music', titre_musiques) #concat artiste
    # filtre additionn > Artiste vers music
    btn_music = st.sidebar.button('RECHERCHE')

# END FILTRE

# INIT LISTE AFTER KNN
if btn_music or "select_music" in st.session_state:
    # SAVE SESSION
    if "select_music" in st.session_state:
        del(st.session_state.select_music)
    if "select_music" in st.session_state:
        val_music = st.session_state.select_music
    else:
        st.session_state.select_music = val_music
    #### TRAITEMENT KNN

    ## LINE FEED SEARCH
    col11, col12= st.columns([2,1])
    with col11:
        # insert jacquet width 30px ######################################## HELP
        st.write('RECHERCHE : ', val_music)
    with col12:
        if st.button('Effacer la recherche'):
            del(st.session_state.select_music)
    
    columns = df.columns.values
    titre_choisi = df[df['track_name'] == val_music]
    titre_choisi_fit = titre_choisi.iloc[0:1, 4:]
    genre_choisi = titre_choisi.iloc[0,0]
    df_cut = df[df['genre'] == genre_choisi]
    X = df_cut[columns[4:]]
    distanceKNN = NearestNeighbors(n_neighbors= 14).fit(X)
    neighbors = distanceKNN.kneighbors(titre_choisi_fit)

    track_id_knn = df_cut.iloc[neighbors[1][0][1:], 3].values

    track_top = track_id_knn[:3]
    track_floor_knn = track_id_knn[3:]
    tracks_floor_chunk_knn = [track_floor_knn[i:i+2] for i in range(0, len(track_floor_knn), 2)]

    # INIT ROW
    st.subheader('TOP 3 : Filtre Music')
    row_top(track_top)
    st.subheader('Vous aimerez certainement aussi ...')
    for bbknn in range(len(tracks_floor_chunk_knn)):
        row_5(tracks_floor_chunk_knn[bbknn])
    # END INIT ROW

### ENF KNN
elif btn_genre  or "select_genre" in st.session_state:
    if "select_genre" in st.session_state:
        del(st.session_state.select_genre)
    # Extraire la plage de durée sélectionnée
    duree_min, duree_max = f_duree
    # Filtrer le dataframe pour cette plage de durée
    filtered_df = df[df['duration_ms'].between(duree_min * 60 * 1000, duree_max * 60 * 1000)]
    # Appliquer le filtre par genre, si des genres ont été sélectionnés
    if f_genre:
        selected_genres = f_genre
        filtered_df = filtered_df[filtered_df["genre"].isin(selected_genres)]
    if f_bpm :
        bpm_min, bpm_max = f_bpm
        filtered_df = filtered_df[df['tempo'].between(bpm_min, bpm_max)].sort_values('popularity', ascending = False)
    # Afficher les résultats
    track_id_genre = filtered_df["track_id"].head(f_r).tolist()

    if "select_genre" not in st.session_state:
        st.session_state.select_genre = track_id_genre
    # SAVE SESSION
    if "select_genre" in st.session_state:
        r_g = st.session_state.select_genre
        track_top = r_g[:3]
        track_floor_knn = r_g[3:]
        tracks_floor_chunk_knn = [track_floor_knn[i:i+2] for i in range(0, len(track_floor_knn), 2)]
    else:
        track_top = track_id_genre[:3]
        track_floor_knn = track_id_genre[3:]
        tracks_floor_chunk_knn = [track_floor_knn[i:i+2] for i in range(0, len(track_floor_knn), 2)]

    # INIT ROW
    st.subheader('TOP 3 : Filtre Genres')
    row_top(track_top)
    st.subheader('vous aimerez certainement aussi ...')
    for bbknn in range(len(tracks_floor_chunk_knn)):
        row_5(tracks_floor_chunk_knn[bbknn])
    # END INIT ROW

else:
    df = df.sort_values('popularity', ascending=False)
    track_id = list(df['track_id'].head(15))
    track_top = track_id[:3]
    track_floor = track_id[3:]
    tracks_floor_chunk = [track_floor[i:i+2] for i in range(0, len(track_floor), 2)]
    # INIT DB
    #create_table()

    # INIT ROW
    st.subheader('Accueil')
    row_top(track_top)
    st.subheader('Les plus populaires du moment')
    for bb in range(len(tracks_floor_chunk)):
        row_5(tracks_floor_chunk[bb])
    # END INIT ROW

# https://open.spotify.com/track/7wqpAYuSk84f0JeqCIETRV?si=09tSut5TyAFiAYSg38gjXE

# Récupérer la clé du bouton cliqué

# add_track_to_playlist(db_conn, track_id)

# Suppression d'une piste de la playlist
# delete_track_from_playlist(db_conn, track_id)

# Fermeture de la connexion à la base de données
db_conn.close()
