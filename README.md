# Multimodal AI Model Exploration & Web Application

This project is built for the assignment **“Multimodal AI Model Exploration & Web Application Development.”**  
It explores multiple AI model providers and input-output modalities including text, image, audio, and video.

## 1. Project Objective

The goal of this project is to test different AI models in a notebook and then build a web application where users can provide text, image, audio, or video inputs and receive AI-generated outputs.

The system supports:

- Text → Text
- Text → Image
- Image → Text
- Audio → Text
- Text → Audio
- Video → Text

## 2. AI Platforms Used

| Platform | Purpose |
|---|---|
| Google Gemini | Text generation, image understanding, video understanding |
| Hugging Face | Text-to-image, speech-to-text, text-to-speech |

## 3. Models Used

| Modality | Model | Provider | Description |
|---|---|---|---|
| Text → Text | `gemini-2.5-flash` | Google Gemini | Generates a text response from a user prompt |
| Text → Image | `stabilityai/stable-diffusion-xl-base-1.0` | Hugging Face | Generates an image from a text prompt |
| Image → Text | `gemini-2.5-flash` | Google Gemini | Describes or answers questions about an uploaded image |
| Audio → Text | `openai/whisper-large-v3-turbo` | Hugging Face | Transcribes uploaded audio into text |
| Text → Audio | `facebook/mms-tts-eng` | Hugging Face | Converts text into spoken audio |
| Video → Text | `gemini-2.5-flash` | Google Gemini | Summarizes or answers questions about uploaded video |

## 4. Project Structure

```text
multimodal_ai_assignment/
│
├── app.py
├── multimodal_ai_notebook.ipynb
├── requirements.txt
├── .env.example
└── README.md
```

## 5. Setup Instructions

### Step 1: Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

For Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

For macOS/Linux:

```bash
source .venv/bin/activate
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Add API keys

Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
HF_TOKEN=your_huggingface_token_here
```

You can get:

- Gemini API key from Google AI Studio
- Hugging Face token from Hugging Face account settings

### Step 4: Run the web application

```bash
streamlit run app.py
```

## 6. Notebook Instructions

Open the notebook:

```bash
jupyter notebook multimodal_ai_notebook.ipynb
```

Run each section one by one:

1. Install/import libraries
2. Load API keys
3. Test Text → Text
4. Test Text → Image
5. Test Image → Text
6. Test Audio → Text
7. Test Text → Audio
8. Test Video → Text

For image, audio, and video tasks, replace the sample file paths with your own files.

## 7. Web Application Features

The Streamlit app provides a dropdown menu where the user can select a modality task.

### Text → Text

User enters a prompt and the Gemini model generates a response.

### Text → Image

User enters an image prompt and Stable Diffusion XL generates an image.

### Image → Text

User uploads an image and asks a question. Gemini analyzes the image and returns a text answer.

### Audio → Text

User uploads audio. Whisper transcribes the speech into text.

### Text → Audio

User enters text. The Hugging Face TTS model generates spoken audio.

### Video → Text

User uploads a short video. Gemini summarizes or answers questions about the video.

## 8. Screenshots to Include in Final Submission

Take screenshots of:

1. Notebook text generation output
2. Notebook image generation output
3. Notebook image analysis output
4. Notebook audio transcription output
5. Notebook video summary output
6. Streamlit homepage
7. Streamlit output for at least 3 modalities

## 9. Demo Video Script

You can record a 2–3 minute demo using this structure:

> Hello, this is my Multimodal AI Model Exploration project.  
> In this project, I used Google Gemini and Hugging Face models to test different input-output modalities.  
> First, I tested each model inside a Jupyter notebook.  
> Then I created a Streamlit web application where users can choose tasks such as text generation, image generation, image analysis, audio transcription, text-to-speech, and video summarization.  
> This demonstrates how modern AI systems can accept different forms of input and produce meaningful outputs across multiple modalities.

## 10. Assignment Requirements Checklist

| Requirement | Status |
|---|---|
| Fresh notebook | Completed |
| Different models from class | Completed, replace if your class used the same ones |
| Multiple modalities | Completed |
| API/local model calls | Completed |
| Sample inputs | Completed |
| Generated outputs | Completed after running |
| Web application | Completed |
| README file | Completed |
| Screenshots/demo video | To be added after running |
| List of models used | Completed |
| Explanation of each modality | Completed |

## 11. Notes

Some Hugging Face models may require provider availability depending on your account and free-tier limits. If one model is unavailable, replace it with another model for the same task from Hugging Face Models.

## 12. Conclusion

This project demonstrates a working multimodal AI system that can process text, image, audio, and video inputs and generate meaningful AI-powered outputs using modern AI model APIs.
