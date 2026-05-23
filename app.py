import os
import time
import wave
from pathlib import Path
from tempfile import NamedTemporaryFile

import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from google import genai
from google.genai import types
from huggingface_hub import InferenceClient

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

st.set_page_config(
    page_title="Multimodal AI Model Explorer",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Multimodal AI Model Explorer")
st.caption("Text, image, audio, and video AI tasks using Gemini + Hugging Face models.")

with st.sidebar:
    st.header("API Status")
    st.write("Gemini API:", "✅ Found" if GEMINI_API_KEY else "❌ Missing")
    st.write("Hugging Face Token:", "✅ Found" if HF_TOKEN else "❌ Missing")

    st.header("Models Used")
    st.markdown(
        """
        - **Text → Text:** Gemini 2.5 Flash
        - **Text → Image:** Stable Diffusion XL via Hugging Face
        - **Image → Text:** Gemini 2.5 Flash
        - **Audio → Text:** Whisper Large v3 Turbo via Hugging Face
        - **Text → Audio:** Gemini TTS
        - **Text → Video:** Stable Diffusion XL + LTX image-to-video pipeline
        - **Video → Text:** Gemini 2.5 Flash
        """
    )

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
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        return tmp.name

def save_pcm_as_wav(filename, pcm_data, channels=1, rate=24000, sample_width=2):
    """Gemini TTS returns raw PCM audio. This function saves it as a playable WAV file."""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm_data)

def wait_for_gemini_file_active(client, uploaded_file, max_wait_seconds=120):
    """
    Gemini video files must become ACTIVE before they can be used for video understanding.
    This prevents FAILED_PRECONDITION errors.
    """
    start_time = time.time()
    file_obj = client.files.get(name=uploaded_file.name)

    while getattr(file_obj, "state", None) and file_obj.state.name == "PROCESSING":
        if time.time() - start_time > max_wait_seconds:
            raise TimeoutError("Video file is still processing. Try a shorter video or retry later.")
        time.sleep(5)
        file_obj = client.files.get(name=uploaded_file.name)

    if getattr(file_obj, "state", None) and file_obj.state.name != "ACTIVE":
        raise RuntimeError(f"Gemini file is not active. Current state: {file_obj.state.name}")

    return file_obj

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

    prompt = st.text_area(
        "Enter your prompt",
        "Explain multimodal AI in simple terms.",
    )

    if st.button("Generate Text"):
        client = get_gemini_client()

        try:
            with st.spinner("Generating text..."):
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
        hf = get_hf_client()

        try:
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
            st.info("Try a shorter prompt or retry later if Hugging Face provider capacity is busy.")

elif task == "Image → Text":
    st.subheader("Image → Text")

    image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    question = st.text_input("Ask something about the image", "Describe this image in detail.")

    if image_file and st.button("Analyze Image"):
        client = get_gemini_client()

        try:
            image = Image.open(image_file)

            with st.spinner("Analyzing image..."):
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
        hf = get_hf_client()

        try:
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
            st.info("Try WAV/MP3 format and keep the audio short for testing.")

elif task == "Text → Audio":
    st.subheader("Text → Audio")

    text = st.text_area(
        "Enter text to convert to speech",
        "Hello, this is a generated audio sample for my multimodal AI assignment.",
    )

    if st.button("Generate Audio"):
        client = get_gemini_client()

        try:
            with st.spinner("Generating audio using Gemini TTS..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash-preview-tts",
                    contents=text,
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
            save_pcm_as_wav(output_path, audio_data)

            st.markdown("### Output")
            st.audio(output_path)

        except Exception as e:
            st.error(f"Text-to-audio failed: {e}")
            st.info("If Gemini TTS is unavailable for your key, use the Audio → Text screenshot and mention this provider limitation.")

elif task == "Text → Video":
    st.subheader("Text → Video")

    prompt = st.text_area(
        "Enter video prompt",
        "A small robot walking through a futuristic classroom, cinematic lighting",
    )

    st.info(
        "This performs Text → Image → Video. The user input is text and the final output is video. "
        "This workaround is used because some Hugging Face providers expose LTX Video as image-to-video instead of direct text-to-video."
    )

    if st.button("Generate Video"):
        hf = get_hf_client()

        try:
            with st.spinner("Step 1/2: Generating starter image from text..."):
                starter_image = hf.text_to_image(
                    prompt,
                    model="stabilityai/stable-diffusion-xl-base-1.0",
                )
                starter_image_path = "text_to_video_starter_image.png"
                starter_image.save(starter_image_path)

            st.markdown("### Generated Starter Image")
            st.image(starter_image, use_container_width=True)

            with st.spinner("Step 2/2: Converting starter image to video. This can take 1–3 minutes..."):
                with open(starter_image_path, "rb") as image_file:
                    video_bytes = hf.image_to_video(
                        image_file.read(),
                        model="Lightricks/LTX-Video-0.9.8-13B-distilled",
                    )

                output_video_path = "generated_video.mp4"
                with open(output_video_path, "wb") as f:
                    f.write(video_bytes)

            st.markdown("### Output Video")
            st.video(output_video_path)

        except Exception as e:
            st.error(f"Text-to-video failed: {e}")
            st.info(
                "This depends on Hugging Face provider availability and credits. "
                "For your assignment, screenshot this error if needed and explain the provider limitation."
            )

elif task == "Video → Text":
    st.subheader("Video → Text")

    video_file = st.file_uploader("Upload a short video", type=["mp4", "mov", "avi"])
    question = st.text_input("Ask something about the video", "Summarize the video in 5 bullet points.")

    if video_file and st.button("Analyze Video"):
        client = get_gemini_client()

        try:
            suffix = Path(video_file.name).suffix
            video_path = save_uploaded_file(video_file, suffix)

            st.video(video_file)

            with st.spinner("Uploading video to Gemini..."):
                uploaded_video = client.files.upload(file=video_path)

            with st.spinner("Waiting for Gemini video file to become ACTIVE..."):
                active_video = wait_for_gemini_file_active(client, uploaded_video)

            with st.spinner("Analyzing video..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[active_video, question],
                )

            st.markdown("### Output")
            st.write(response.text)

        except Exception as e:
            st.error(f"Video analysis failed: {e}")
            st.info("Try a shorter MP4 video and wait a few seconds before retrying.")
