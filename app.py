import os
import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from google import genai
from huggingface_hub import InferenceClient

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

st.set_page_config(page_title="Multimodal AI Model Explorer", page_icon="🤖", layout="wide")

st.title("🤖 Multimodal AI Model Explorer")
st.caption("Text, image, audio, and video AI tasks using Gemini + Hugging Face models.")

with st.sidebar:
    st.header("API Status")
    st.write("Gemini API:", "✅ Found" if GEMINI_API_KEY else "❌ Missing")
    st.write("Hugging Face Token:", "✅ Found" if HF_TOKEN else "❌ Missing")

    st.header("Models Used")
    st.markdown("""
    - **Text → Text:** Gemini 2.5 Flash
    - **Image → Text:** Gemini 2.5 Flash
    - **Audio → Text:** OpenAI Whisper Large v3 Turbo via Hugging Face
    - **Video → Text:** Gemini 2.5 Flash
    - **Text → Image:** Stable Diffusion XL via Hugging Face
    - **Text → Audio:** Facebook MMS TTS English via Hugging Face
    """)

def get_gemini_client():
    if not GEMINI_API_KEY:
        st.error("Missing GEMINI_API_KEY. Add it to your .env file.")
        st.stop()
    return genai.Client(api_key=GEMINI_API_KEY)

def get_hf_client():
    if not HF_TOKEN:
        st.error("Missing HF_TOKEN. Add it to your .env file.")
        st.stop()
    return InferenceClient(token=HF_TOKEN)

def save_uploaded_file(uploaded_file, suffix):
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        return tmp.name

task = st.selectbox(
    "Choose a modality task",
    [
        "Text → Text",
        "Text → Image",
        "Image → Text",
        "Audio → Text",
        "Text → Audio",
        "Video → Text",
    ],
)

if task == "Text → Text":
    st.subheader("Text → Text")
    prompt = st.text_area("Enter your prompt", "Explain multimodal AI in simple terms.")
    if st.button("Generate Text"):
        client = get_gemini_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        st.markdown("### Output")
        st.write(response.text)

elif task == "Text → Image":
    st.subheader("Text → Image")
    prompt = st.text_area(
        "Enter image prompt",
        "A futuristic classroom where students use multimodal AI tools, cinematic lighting",
    )
    if st.button("Generate Image"):
        hf = get_hf_client()
        image = hf.text_to_image(
            prompt,
            model="stabilityai/stable-diffusion-xl-base-1.0",
        )
        st.markdown("### Output")
        st.image(image, caption="Generated image", use_container_width=True)

elif task == "Image → Text":
    st.subheader("Image → Text")
    image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    question = st.text_input("Ask something about the image", "Describe this image in detail.")
    if image_file and st.button("Analyze Image"):
        client = get_gemini_client()
        image = Image.open(image_file)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[question, image],
        )
        st.image(image, caption="Uploaded image", use_container_width=True)
        st.markdown("### Output")
        st.write(response.text)

elif task == "Audio → Text":
    st.subheader("Audio → Text")
    audio_file = st.file_uploader("Upload audio", type=["wav", "mp3", "m4a"])
    if audio_file and st.button("Transcribe Audio"):
        hf = get_hf_client()
        suffix = Path(audio_file.name).suffix
        audio_path = save_uploaded_file(audio_file, suffix)
        result = hf.automatic_speech_recognition(
            audio_path,
            model="openai/whisper-large-v3-turbo",
        )
        st.audio(audio_file)
        st.markdown("### Output")
        st.write(result.get("text", result) if isinstance(result, dict) else result)

elif task == "Text → Audio":
    st.subheader("Text → Audio")
    text = st.text_area("Enter text to convert to speech", "Hello, this is a generated audio sample.")
    if st.button("Generate Audio"):
        hf = get_hf_client()
        audio_bytes = hf.text_to_speech(
            text,
            model="facebook/mms-tts-eng",
        )
        output_path = "generated_audio.wav"
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
        st.markdown("### Output")
        st.audio(output_path)

elif task == "Video → Text":
    st.subheader("Video → Text")
    video_file = st.file_uploader("Upload a short video", type=["mp4", "mov", "avi"])
    question = st.text_input("Ask something about the video", "Summarize the video in 5 bullet points.")
    if video_file and st.button("Analyze Video"):
        client = get_gemini_client()
        suffix = Path(video_file.name).suffix
        video_path = save_uploaded_file(video_file, suffix)

        uploaded_video = client.files.upload(file=video_path)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[uploaded_video, question],
        )
        st.video(video_file)
        st.markdown("### Output")
        st.write(response.text)
