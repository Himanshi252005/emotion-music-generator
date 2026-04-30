# Emotion-Aware Music Generator

An AI-powered web application that detects facial emotions and recommends 
personalized YouTube playlists in real time.

## Demo


Live demo: https://duffel-unlinked-unbalance.ngrok-free.dev
(Hosted locally — may be offline)

## How It Works
1. User uploads a facial photo through the Streamlit interface
2. DeepFace analyzes the image and classifies the dominant emotion
3. The detected emotion maps to a curated music query
4. YouTube Data API v3 returns real-time song recommendations

## Tech Stack
- **Emotion Detection:** DeepFace (CNN-based facial recognition)
- **Image Processing:** OpenCV
- **Music Retrieval:** YouTube Data API v3
- **Web Interface:** Streamlit
- **Language:** Python 3.13

## Supported Emotions
Happy, Sad, Angry, Fear, Surprise, Neutral, Disgust — each mapped to a 
distinct musical genre.

## Setup
\```bash
git clone https://github.com/Himanshi252005/emotion-music-generator.git
cd emotion-music-generator
pip install -r requirements.txt
\```

Create a `.env` file with your YouTube API key:
\```
YOUTUBE_API_KEY=your_key_here
\```

Run the application:
\```bash
streamlit run app.py
\```

## Project Phases
- Phase 1: Emotion detection prototype (Jupyter)
- Phase 2: YouTube API integration
- Phase 3: End-to-end pipeline
- Phase 4: Streamlit UI
- Phase 5: Live deployment via ngrok

## Author
Himanshi — [LinkedIn](www.linkedin.com/in/himanshi-rathore-hr2520)
