import os
import streamlit as st
import cv2
import matplotlib.pyplot as plt
from fer import FER
from googleapiclient.discovery import build
import numpy as np
from PIL import Image

API_KEY = os.getenv("YOUTUBE_API_KEY")

emotion_to_query = {
    "happy":    "happy upbeat pop music",
    "sad":      "sad acoustic emotional music",
    "angry":    "intense powerful rock music",
    "fear":     "calm relaxing ambient music",
    "surprise": "exciting electronic EDM music",
    "neutral":  "lofi chill study music",
    "disgust":  "peaceful classical music"
}

emotion_emoji = {
    "happy":    "😊",
    "sad":      "😢",
    "angry":    "😠",
    "fear":     "😨",
    "surprise": "😲",
    "neutral":  "😐",
    "disgust":  "🤢"
}

emotion_color = {
    "happy":    "#FFD700",
    "sad":      "#4169E1",
    "angry":    "#FF4500",
    "fear":     "#9370DB",
    "surprise": "#00CED1",
    "neutral":  "#808080",
    "disgust":  "#228B22"
}

st.set_page_config(
    page_title="Emotion Music Generator",
    page_icon="🎵",
    layout="centered"
)

st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        background: linear-gradient(90deg, #f953c6, #b91d73);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 16px;
        margin-bottom: 30px;
    }
    .song-card {
        background-color: #1e1e2e;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #f953c6;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🎵 Emotion Music Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your face picks the music. No playlist needed.</p>', unsafe_allow_html=True)
st.divider()

def detect_emotion(frame):
    try:
        detector = FER(mtcnn=False)
        result = detector.detect_emotions(frame)
        if result:
            emotions = result[0]['emotions']
            dominant = max(emotions, key=emotions.get)
            return dominant, emotions
        return "neutral", {}
    except:
        return "neutral", {}

def get_songs(emotion):
    try:
        youtube = build("youtube", "v3", developerKey=API_KEY)
        query = emotion_to_query.get(emotion, "relaxing music")
        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=5,
            videoCategoryId="10"
        )
        response = request.execute()
        songs = []
        for item in response["items"]:
            songs.append({
                "title":   item["snippet"]["title"].replace("&#39;", "'").replace("&amp;", "&"),
                "channel": item["snippet"]["channelTitle"],
                "url":     f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            })
        return songs
    except:
        return []

st.subheader("📸 Step 1 — Capture Your Face")
img_file = st.camera_input("Look at the camera and click!")

if img_file is not None:
    image = Image.open(img_file)
    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    with st.spinner("🔍 Analyzing your emotion..."):
        dominant_emotion, all_emotions = detect_emotion(frame)

    emoji = emotion_emoji.get(dominant_emotion, "😐")
    color = emotion_color.get(dominant_emotion, "#888")

    st.divider()
    st.subheader("🧠 Step 2 — Your Emotion")
    st.markdown(
        f'<div style="text-align:center; padding:20px; border-radius:15px; '
        f'background-color:{color}22; border: 2px solid {color}; '
        f'font-size:28px; font-weight:bold;">'
        f'{emoji} You look <span style="color:{color}">{dominant_emotion.upper()}</span> right now!'
        f'</div>',
        unsafe_allow_html=True
    )

    if all_emotions:
        fig, ax = plt.subplots(figsize=(8, 3))
        fig.patch.set_facecolor('#0e1117')
        ax.set_facecolor('#0e1117')
        emotions = list(all_emotions.keys())
        scores = list(all_emotions.values())
        bar_colors = [color if e == dominant_emotion else '#444' for e in emotions]
        ax.barh(emotions, scores, color=bar_colors)
        ax.set_xlabel('Confidence', color='white')
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('#444')
        ax.spines['left'].set_color('#444')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)

    st.divider()
    st.subheader("🎵 Step 3 — Your Mood Playlist")

    with st.spinner("🎵 Finding perfect songs for you..."):
        songs = get_songs(dominant_emotion)

    if songs:
        for i, song in enumerate(songs, 1):
            st.markdown(
                f'<div class="song-card">'
                f'<b>{i}. {song["title"]}</b><br>'
                f'<small>📺 {song["channel"]}</small><br>'
                f'<a href="{song["url"]}" target="_blank">▶️ Play on YouTube</a>'
                f'</div>',
                unsafe_allow_html=True
            )
    else:
        st.error("Could not fetch songs. Check your API key in secrets.")

    st.divider()
    st.success("✅ Done! Enjoy your music! 🎧")
    st.balloons()
