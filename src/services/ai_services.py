import os
import shutil
import yt_dlp
import google.generativeai as genai
from huggingface_hub import InferenceClient
from src.config import GOOGLE_AI_API_KEY, HF_API_KEY, HF_ASR_MODEL, GEMINI_MODEL_NAME


class AIService:
    def __init__(self):
        if not GOOGLE_AI_API_KEY or GOOGLE_AI_API_KEY == "YOUR_GOOGLE_AI_STUDIO_API_KEY":
            print("Warning: Google AI API key not set. AI formatting will be disabled.")
            self.gemini_model = None
        else:
            genai.configure(api_key=GOOGLE_AI_API_KEY)
            self.gemini_model = genai.GenerativeModel(GEMINI_MODEL_NAME)

        if not HF_API_KEY:
            self.hf_client = None
            print("Warning: Hugging Face API key (HF_API_KEY) is not set. AI transcription will be disabled.")
        else:
            self.hf_client = InferenceClient(
                provider="hf-inference",
                api_key=HF_API_KEY,
                headers={"Content-Type": "audio/webm;codecs=opus"}
            )

    def transcribe_audio_hf(self, youtube_url):
        """
        Downloads audio from a YouTube URL and transcribes it using Hugging Face's Inference API.
        """
        if not self.hf_client:
            print("Cannot transcribe: Hugging Face client is not configured.")
            return None

        audio_path, save_dir = self._download_audio(youtube_url)
        if not audio_path:
            return None

        try:
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()

            transcription = self.hf_client.automatic_speech_recognition(
                audio_bytes,
                model=HF_ASR_MODEL
            )
            return transcription.get("text", None)


        except Exception as e:
            print(f"Error during transcription with Hugging Face: {e}")
            return None
        finally:
            # Clean up the temporary audio files
            if save_dir and os.path.exists(save_dir):
                shutil.rmtree(save_dir)


    def _download_audio(self, url):
        """Downloads the audio track of a YouTube video to a temporary location."""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            save_path = os.path.join(current_dir, 'audio_temp')
            os.makedirs(save_path, exist_ok=True)
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(save_path, 'audio.%(ext)s'),
                'noplaylist': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'opus',
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                base_path = ydl.prepare_filename(info).rsplit('.', 1)[0]
                final_path = base_path + '.opus'

            if os.path.exists(final_path):
                return final_path, save_path

            # Fallback if the path logic fails for some reason
            if os.path.exists(base_path + '.webm'):
                return base_path + '.webm', save_path

            return None, save_path
        except Exception as e:
            print(f"Error downloading audio: {e}")
            return None, None

    def format_text_gemini(self, text_to_format):
        """Uses Google's Gemini model to format text."""
        if not self.gemini_model:
            print("AI formatting skipped: Google AI API key not configured.")
            return None
        prompt = f"""Please format the following text. Correct grammar, spelling, and punctuation. 
Organize it into sensible paragraphs. Do not add or remove any information or change the original meaning.
Return only the formatted text.

Original Text:
---
{text_to_format}
---
"""
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error with Gemini formatting: {e}")
            return None