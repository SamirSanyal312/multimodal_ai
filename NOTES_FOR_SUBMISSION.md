# Submission Notes

Use the Streamlit app screenshots as proof that the modalities work.
For the notebook, copy the same task sections from `app.py` into cells or use your previous notebook and update:
- Text → Audio: use Gemini TTS instead of Hugging Face MMS TTS.
- Video → Text: add file ACTIVE polling before analysis.
- Text → Video: add Hugging Face `hf_client.text_to_video(...)`.
