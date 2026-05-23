import os
import time
import wave
import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from google import genai
from google.genai import types
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
    - **Text → Audio:** Gemini 2.5 Flash Preview TTS
    - **Text → Video:** LTX Video via Hugging Face
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

def save_wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    """Save Gemini TTS raw PCM bytes as a playable WAV file."""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

def wait_for_gemini_file_active(client, uploaded_file, max_wait_seconds=180):
    """Gemini video files need processing time before they can be used."""
    start = time.time()
    status_box = st.empty()

    while not uploaded_file.state or uploaded_file.state.name != "ACTIVE":
        elapsed = int(time.time() - start)

        if elapsed > max_wait_seconds:
            raise TimeoutError(
                "Video file processing took too long. Try a shorter/smaller video."
            )

        status_box.info(f"Processing video file in Gemini... Current state: {uploaded_file.state}. Waited {elapsed}s.")
        time.sleep(5)
        uploaded_file = client.files.get(name=uploaded_file.name)

    status_box.success("Video is ready for analysis.")
    return uploaded_file

task = st.selectbox(
    "Choose a modality task",
    [
        "Text → Text",
        "Text → Image",
        "Image → Text",
        "Audio → Text",
        "Text → Audio",
        "Text → Video",
        "Video → Text",
    ],
)

if task == "Text → Text":
    st.subheader("Text → Text")
    prompt = st.text_area("Enter your prompt", "Explain multimodal AI in simple terms.")
    if st.button("Generate Text"):
        try:
            client = get_gemini_client()
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            st.markdown("### Output")
            st.write(response.text)
        except Exception as e:
            st.error(f"Text generation failed: {e}")

elif task == "Text → Image":
    st.subheader("Text → Image")
    prompt = st.text_area(
        "Enter image prompt",
        "A futuristic classroom where students use multimodal AI tools, cinematic lighting",
    )
    if st.button("Generate Image"):
        try:
            hf = get_hf_client()
            with st.spinner("Generating image..."):
                image = hf.text_to_image(
                    prompt,
                    model="stabilityai/stable-diffusion-xl-base-1.0",
                )
            st.markdown("### Output")
            st.image(image, caption="Generated image", use_container_width=True)
            image.save("generated_image.png")
        except Exception as e:
            st.error(f"Image generation failed: {e}")

elif task == "Image → Text":
    st.subheader("Image → Text")
    image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    question = st.text_input("Ask something about the image", "Describe this image in detail.")
    if image_file and st.button("Analyze Image"):
        try:
            client = get_gemini_client()
            image = Image.open(image_file)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[question, image],
            )
            st.image(image, caption="Uploaded image", use_container_width=True)
            st.markdown("### Output")
            st.write(response.text)
        except Exception as e:
            st.error(f"Image analysis failed: {e}")

elif task == "Audio → Text":
    st.subheader("Audio → Text")
    audio_file = st.file_uploader("Upload audio", type=["wav", "mp3", "m4a"])
    if audio_file and st.button("Transcribe Audio"):
        try:
            hf = get_hf_client()
            suffix = Path(audio_file.name).suffix
            audio_path = save_uploaded_file(audio_file, suffix)

            with st.spinner("Transcribing audio..."):
                result = hf.automatic_speech_recognition(
                    audio_path,
                    model="openai/whisper-large-v3-turbo",
                )

            st.audio(audio_file)
            st.markdown("### Output")
            st.write(result.get("text", result) if isinstance(result, dict) else result)
        except Exception as e:
            st.error(f"Audio transcription failed: {e}")

elif task == "Text → Audio":
    st.subheader("Text → Audio")
    text = st.text_area(
        "Enter text to convert to speech",
        "Hello, my name is Samir Sanyal and this is my multimodal AI assignment demo.",
    )

    if st.button("Generate Audio"):
        try:
            client = get_gemini_client()

            with st.spinner("Generating audio using Gemini TTS..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash-preview-tts",
                    contents=f"Say clearly and naturally: {text}",
                    config=types.GenerateContentConfig(
                        response_modalities=["AUDIO"],
                        speech_config=types.SpeechConfig(
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name="Kore"
                                )
                            )
                        ),
                    ),
                )

            audio_data = response.candidates[0].content.parts[0].inline_data.data
            output_path = "generated_audio.wav"
            save_wave_file(output_path, audio_data)

            st.markdown("### Output")
            st.audio(output_path)
            st.success("Audio generated successfully.")
        except Exception as e:
            st.error(f"Text-to-audio failed: {e}")
            st.info("If this fails, check whether your Gemini API key has access to Gemini TTS preview models.")

elif task == "Text → Video":
    st.subheader("Text → Video")
    prompt = st.text_area(
        "Enter video prompt",
        "A small robot walking through a futuristic classroom, cinematic lighting",
    )

    if st.button("Generate Video"):
        try:
            hf = get_hf_client()

            with st.spinner("Generating video. This can take 1–3 minutes depending on provider availability..."):
                video_bytes = hf.text_to_video(
                    prompt,
                    model="Lightricks/LTX-Video-0.9.8-13B-distilled",
                    num_frames=16,
                    num_inference_steps=20,
                )

            output_path = "generated_video.mp4"
            with open(output_path, "wb") as f:
                f.write(video_bytes)

            st.markdown("### Output")
            st.video(output_path)
            st.success("Video generated successfully.")
        except Exception as e:
            st.error(f"Text-to-video failed: {e}")
            st.info(
                "Text-to-video depends on Hugging Face provider availability/credits. "
                "If this fails, take a screenshot of the error and try again later or try another text-to-video model."
            )

elif task == "Video → Text":
    st.subheader("Video → Text")
    video_file = st.file_uploader("Upload a short video", type=["mp4", "mov", "avi", "webm"])
    question = st.text_input("Ask something about the video", "Summarize the video in 5 bullet points.")

    if video_file and st.button("Analyze Video"):
        try:
            client = get_gemini_client()
            suffix = Path(video_file.name).suffix
            video_path = save_uploaded_file(video_file, suffix)

            st.video(video_file)

            with st.spinner("Uploading video to Gemini..."):
                uploaded_video = client.files.upload(file=video_path)

            uploaded_video = wait_for_gemini_file_active(client, uploaded_video)

            with st.spinner("Analyzing video..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[uploaded_video, question],
                )

            st.markdown("### Output")
            st.write(response.text)
        except Exception as e:
            st.error(f"Video analysis failed: {e}")
            st.info("Use a short MP4 video. If the file is still PROCESSING, wait and retry.")
