import re
import pandas as pd
from math import sqrt
import streamlit as st
from streamlit_float import *
from Topsis import Topsis

def display_recommendation(iframe_code, percentage):
    st.markdown(f"This song matches your taste by **{percentage * 100:.3f}%**")
    st.progress(percentage)
    st.markdown(iframe_code, unsafe_allow_html=True)

def main():
    if 'searched' not in st.session_state:
        st.session_state.searched = False

    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    def click_button():
        st.session_state.clicked = True

    if 'preVal_w' and 'preVal_i' not in st.session_state:
        st.session_state.preVal_w = [0] * 9
        st.session_state.preVal_i = [0] * 9

    if 'val_w' and 'val_i' not in st.session_state:
        st.session_state.val_w = [0] * 9
        st.session_state.val_i = [0] * 9
    
    
    weight = [0] * 9
    impact = [0] * 9
    st.markdown("<h1 style='text-align: center; color: black;'><span style='color: #1DB954;'>Music</span> Recommendation System Using TOPSIS</h1>", unsafe_allow_html=True)    
    st.markdown("<p style='text-align: center; color: black;'>by <b>Rizky Ramadhan Sudjarmono</b> (210004), <b>Ardes Zubka Putra</b> (210009), <b>Raditya Muhamad Lacavi</b> (210019), and <b>Akmal Azzary Megaputra</b> (210048) to fulfill the final exam of the Decision Support System class</p>", unsafe_allow_html=True)
    genre = st.sidebar.selectbox("What type of song do you want to listen to?", ['English', 'Indonesia', 'Japan', 'Korea'])

    st.sidebar.markdown("<h3 style='text-align: center; color: black;'>Select your <span style='text-decoration: underline; text-decoration-color: #1DB954;'>preferences</span></h3>", unsafe_allow_html=True)
    attributes = ["Acousticness🎻", "Danceability💃", "Energy⚡", "Instrumentalness🎼", "Liveness🎙️", "Loudness🔉", "Speechiness🗣️", "Tempo⏩", "Valence😊"]
    descriptions = [
        "A confidence measure whether the track is acoustic. 10 represents high confidence the track is acoustic.",
        "How suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. 10 represents high confidence the track is danceable.",
        "A perceptual measure of intensity and activity. 10 represents high confidence the track is energetic.",
        "Predicts whether a track contains no vocals. 10 represents high confidence the track contains no vocals.",
        "Detects the presence of an audience in the recording. 10 represents high confidence the track is live.",
        "The overall loudness of a track in decibels (dB). 10 represents high confidence the track is loud.",
        "Detects the presence of spoken words in a track. 10 represents high confidence the track contains no speech.",
        "The overall estimated tempo of a track in beats per minute (BPM). 10 represents high confidence the track is fast.",
        "Describing the musical positiveness conveyed by a track. 10 represents high confidence the track is positive."
    ]

    for i in range(len(attributes)):
        st.sidebar.markdown(f"<h4 style='color: #1DB954; font-weight: bold;'>{attributes[i]}</h4>", unsafe_allow_html=True)
        weight[i] = st.sidebar.slider(descriptions[i], -10, 10, 0)
        impact[i] = 1 if weight[i] >= 0 else 0
        weight[i] = abs(weight[i])
        st.session_state.preVal_w[i] = weight[i]
        st.session_state.preVal_i[i] = impact[i]
    st.sidebar.markdown("***")


    float_init()
    float_container = st.sidebar.container()
    with float_container:   
        if weight != [0] * 9:
            button = float_container.button("Search", on_click=click_button, disabled = False, use_container_width = True)
        else:
            error = float_container.error("Please change at least one preference!")
            button = float_container.button("Search", on_click=click_button, disabled = True, use_container_width = True)
       
    float_container.float("bottom: 0; background-color: #f0f2f6; padding: 0px 0px 20px")

    if st.session_state.clicked == True:
        data = pd.read_csv(f'data/{genre}.csv')
        topsis = Topsis(data, st.session_state.preVal_w, st.session_state.preVal_i)
        

        for i in range(0, 9):    
            st.session_state.val_w[i] = st.session_state.preVal_w[i]
            st.session_state.val_i[i] = st.session_state.preVal_i[i]

        st.session_state.clicked = False
        st.session_state.searched = True

    if st.session_state.searched == False:
        st.markdown("<h4 style='text-align: center; color: black;'>↖️ You haven't searched for a song yet, head to the sidebar!</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: black;'>How about recommendation of the day 👇</h4>", unsafe_allow_html=True)
        st.markdown("02:01")
        korea = pd.read_csv(f'data/Korea Trimmed.csv')
        sample = korea.iloc[[100]]
        # embed = re.compile(r'https://open.spotify.com/track/(\w+)').sub(r'https://open.spotify.com/embed/track/\1', sample['trackUrl'].values[0])
        # iframe_code = f'<iframe style="border-radius:12px; background-color: transparent;" src="{embed}?utm_source=generator" width="100%" height="160" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'
        # st.markdown(f"It's **{sample['trackName'].values[0]}** by **{sample['artistName'].values[0]}**")
        iframe_code = f'<iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/00Coyxt9mTec1acC52qtWa?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'
        st.markdown(iframe_code, unsafe_allow_html=True)
    else :
        data = pd.read_csv(f'data/{genre}.csv')
        topsis = Topsis(data, st.session_state.val_w, st.session_state.val_i)
        topsis.run()
        rec = topsis.getEmbed()
        percent = topsis.getPercentage()

        for i, percentage in zip(rec, percent):
            iframe_code = f'<iframe style="border-radius:12px; background-color: transparent;" src="{i}?utm_source=generator" width="100%" height="160" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'
            display_recommendation(iframe_code, percentage)


if __name__ == '__main__':
    main()