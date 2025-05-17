import streamlit as st
import openai
from gtts import gTTS
import os
from io import BytesIO
from PIL import Image
import requests

st.set_page_config(page_title="Emotion-Driven Story Generator", page_icon="🎭")

# --- OpenAI API key input ---
if "OPENAI_API_KEY" not in st.secrets:
    st.warning("Please add your OpenAI API key in Streamlit secrets (openai_api_key)")
    st.stop()
    
openai.api_key = st.secrets["openai_api_key"]

st.title("🎭 Emotion-Driven Story Generator")

# Step 1: Choose your emotion
emotion = st.selectbox("How are you feeling today?", ["Happy", "Sad", "Anxious", "Excited", "Angry", "Lonely", "Curious"])

# Step 2: Generate Story button
if st.button("Generate Story"):
    with st.spinner("Generating story..."):
        # Generate story using GPT-3.5
        prompt = (
            f"Write a short, creative, and inspiring story that reflects the emotion: {emotion}. "
            "Make it comforting and uplifting."
        )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.8,
        )
        story = response['choices'][0]['message']['content']
        st.markdown("### Your Story:")
        st.write(story)

        # Generate image using DALL·E
        st.spinner("Generating image...")
        img_response = openai.Image.create(
            prompt=f"{emotion} emotion, storytelling, artistic, vibrant colors",
            n=1,
            size="512x512"
        )
        img_url = img_response['data'][0]['url']
        image = Image.open(requests.get(img_url, stream=True).raw)
        st.image(image, caption=f"Art inspired by the emotion: {emotion}")

        # Generate voice narration with gTTS
        st.spinner("Generating voice narration...")
        tts = gTTS(text=story, lang='en')
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        st.audio(mp3_fp, format='audio/mp3')

st.markdown("---")
st.write("Made with ❤️ by you — powered by OpenAI GPT-3.5 and DALL·E, narrated by gTTS.")
