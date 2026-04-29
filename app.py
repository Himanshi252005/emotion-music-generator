import streamlit as st
import cv2
from deepface import DeepFace
import matplotlib.pyplot as plt
from googleapiclient.discovery import build
import numpy as np
from PIL import Image

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
import os
API_KEY = os.getenv("YOUTUBE_API_KEY")
# API_KEY = "AIzaSyAuNDwNbbk29vxtN1foHMGGJqcu9vr0mlc"

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

# ─────────────────────────────────────────
# PAGE SETUP
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Emotion Music Generator",
    page_icon="🎵",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
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
    .emotion-box {
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        font-size: 28px;
        font-weight: bold;
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

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown('<p class="title">🎵 Emotion Music Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your face picks the music. No playlist needed.</p>', unsafe_allow_html=True)
st.divider()

# ─────────────────────────────────────────
# FUNCTIONS
# ─────────────────────────────────────────
def detect_emotion(frame):
    try:
        result = DeepFace.analyze(
            frame,
            actions=['emotion'],
            enforce_detection=False
        )
        return result[0]['dominant_emotion'], result[0]['emotion']
    except:
        return "neutral", {}

def get_songs(emotion):
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

# ─────────────────────────────────────────
# WEBCAM CAPTURE
# ─────────────────────────────────────────
st.subheader("📸 Step 1 — Capture Your Face")
img_file = st.camera_input("Look at the camera and click!")

if img_file is not None:

    # Convert to OpenCV format
    image = Image.open(img_file)
    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # ── Detect Emotion ──
    with st.spinner("🔍 Analyzing your emotion..."):
        dominant_emotion, all_emotions = detect_emotion(frame)

    emoji = emotion_emoji.get(dominant_emotion, "😐")
    color = emotion_color.get(dominant_emotion, "#888")

    # ── Show Emotion ──
    st.divider()
    st.subheader("🧠 Step 2 — Your Emotion")
    st.markdown(
        f'<div class="emotion-box" style="background-color:{color}22; border: 2px solid {color};">'
        f'{emoji} You look <span style="color:{color}">{dominant_emotion.upper()}</span> right now!'
        f'</div>',
        unsafe_allow_html=True
    )

    # ── Emotion Chart ──
    fig, ax = plt.subplots(figsize=(8, 3))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    emotions = list(all_emotions.keys())
    scores = list(all_emotions.values())
    bar_colors = [color if e == dominant_emotion else '#444' for e in emotions]
    ax.barh(emotions, scores, color=bar_colors)
    ax.set_xlabel('Confidence %', color='white')
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('#444')
    ax.spines['left'].set_color('#444')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    st.pyplot(fig)

    # ── Get Songs ──
    st.divider()
    st.subheader("🎵 Step 3 — Your Mood Playlist")

    with st.spinner("🎵 Finding perfect songs for you..."):
        songs = get_songs(dominant_emotion)

    for i, song in enumerate(songs, 1):
        st.markdown(
            f'<div class="song-card">'
            f'<b>{i}. {song["title"]}</b><br>'
            f'<small>📺 {song["channel"]}</small><br>'
            f'<a href="{song["url"]}" target="_blank">▶️ Play on YouTube</a>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.divider()
    st.success("✅ Done! Enjoy your music! 🎧")
    st.balloons()