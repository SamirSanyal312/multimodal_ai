# Multimodal AI Model Explorer

This Streamlit app demonstrates multiple AI input/output modalities for the assignment.

## Modalities

| Modality | Model | Provider |
|---|---|---|
| Text → Text | gemini-2.5-flash | Google Gemini |
| Text → Image | stabilityai/stable-diffusion-xl-base-1.0 | Hugging Face |
| Image → Text | gemini-2.5-flash | Google Gemini |
| Audio → Text | openai/whisper-large-v3-turbo | Hugging Face |
| Text → Audio | gemini-2.5-flash-preview-tts | Google Gemini |
| Text → Video | Lightricks/LTX-Video-0.9.8-13B-distilled | Hugging Face |
| Video → Text | gemini-2.5-flash | Google Gemini |

## Why this version was updated

- Text → Audio was changed from Hugging Face MMS TTS to Gemini TTS because Hugging Face may return provider availability errors for some TTS models.
- Video → Text now waits until the uploaded Gemini file becomes ACTIVE before calling the model.
- Text → Video was added using Hugging Face `InferenceClient.text_to_video`.

## Setup

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
HF_TOKEN=your_huggingface_token_here
```

Run:

```bash
streamlit run app.py
```

## Screenshots to submit

Include screenshots for:

1. Text → Text
2. Text → Image
3. Image → Text
4. Audio → Text
5. Text → Audio
6. Text → Video
7. Video → Text
