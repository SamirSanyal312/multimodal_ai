# Multimodal AI Model Exploration & Web Application

This project is for the assignment **Multimodal AI Model Exploration & Web Application Development**.

The project explores different AI input-output modalities and provides both:

1. A Jupyter notebook for model testing.
2. A Streamlit web application for interactive multimodal input and output.

## Features

The application supports:

- Text → Text
- Text → Image
- Image → Text
- Audio → Text
- Text → Audio
- Text → Video
- Video → Text

## Platforms Used

| Platform | Usage |
|---|---|
| Google Gemini | Text generation, image analysis, text-to-audio, video analysis |
| Hugging Face | Text-to-image, audio transcription, image-to-video pipeline |

## Models Used

| Modality | Model | Provider | Purpose |
|---|---|---|---|
| Text → Text | `gemini-2.5-flash` | Google Gemini | Generates text responses |
| Text → Image | `stabilityai/stable-diffusion-xl-base-1.0` | Hugging Face | Generates images from text prompts |
| Image → Text | `gemini-2.5-flash` | Google Gemini | Describes or answers questions about images |
| Audio → Text | `openai/whisper-large-v3-turbo` | Hugging Face | Transcribes audio into text |
| Text → Audio | `gemini-2.5-flash-preview-tts` | Google Gemini | Converts text into speech |
| Text → Video | SDXL + `Lightricks/LTX-Video-0.9.8-13B-distilled` | Hugging Face | Converts text prompt into image, then image into video |
| Video → Text | `gemini-2.5-flash` | Google Gemini | Summarizes and describes uploaded video |

## Project Structure

```text
multimodal_ai_assignment_v3_working/
│
├── app.py
├── multimodal_ai_notebook.ipynb
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Setup Instructions

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the environment

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env`

Copy `.env.example` and rename it to `.env`.

Add your keys:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
HF_TOKEN=your_huggingface_token_here
```

### 5. Run the Streamlit app

```bash
streamlit run app.py
```

## Modality Explanation

### Text → Text

The user enters a text prompt. Gemini generates a natural language response.

Example:

```text
Explain multimodal AI in simple terms.
```

### Text → Image

The user enters an image prompt. Stable Diffusion XL generates an image.

Example:

```text
A futuristic classroom where students use multimodal AI tools.
```

### Image → Text

The user uploads an image and asks a question. Gemini analyzes the image and returns a description or answer.

Example:

```text
Describe this image in detail.
```

### Audio → Text

The user uploads audio. Whisper transcribes the speech into text.

Example:

```text
Uploaded MP3/WAV file → written transcript.
```

### Text → Audio

The user enters text. Gemini TTS generates a playable WAV audio file.

Example:

```text
Hello, this is my multimodal AI assignment.
```

### Text → Video 

This directly generates a video from a text prompt using the Hugging Face model `Wan-AI/Wan2.2-TI2V-5B` through the `fal-ai` inference provider.

### Video → Text

The user uploads a short video. Gemini waits until the uploaded file becomes active and then summarizes the video.

Example:

```text
Summarize this video in 5 bullet points.
```

## Screenshots to Include

For final submission, take screenshots of:

1. Streamlit homepage
2. Text → Text output
3. Text → Image output
4. Image → Text output
5. Audio → Text output
6. Text → Audio output
7. Text → Video output or provider limitation screenshot
8. Video → Text output
9. Notebook outputs

## Demo Video Script

You can use this script while recording your demo:

```text
Hello, this is my Multimodal AI Model Exploration project.

In this project, I explored multiple AI input-output modalities using Google Gemini and Hugging Face models.

The application supports text generation, image generation, image understanding, audio transcription, text-to-speech, text-to-video, and video summarization.

I first tested these models inside a Jupyter notebook. Then I built a Streamlit web application where users can choose a modality task and provide text, image, audio, or video input.

For text-to-video, I used a two-step pipeline where the text prompt creates a starter image, and the image is converted into video.

This project shows how modern AI systems can process multiple forms of input and generate useful outputs across text, image, audio, and video.
```

## Assignment Checklist

| Requirement | Status |
|---|---|
| Fresh notebook | Completed |
| Web application | Completed |
| Text input support | Completed |
| Image upload support | Completed |
| Audio upload support | Completed |
| Video upload support | Completed |
| Text response output | Completed |
| Generated image output | Completed |
| Generated audio output | Completed |
| Transcribed text output | Completed |
| Generated video output | Completed through text-image-video pipeline |
| Video summary output | Completed |
| README file | Completed |
| Model list | Completed |
| Modality explanations | Completed |
| Screenshots/demo video | To be added after running |

## Notes

Some Hugging Face video models depend on provider availability and free-tier credits. If Text → Video fails, take a screenshot of the error and mention provider limitation in your submission. The rest of the app will continue working independently.
