# Youtube Transcript Extractor

A Python command-line tool to fetch transcripts from YouTube videos, channels, or playlists. The application can save the output to Google Docs or a local Microsoft Word file, with options for AI-powered transcription and text formatting.

## Key Features

-   **Multiple Sources**: Extract transcripts from single videos, entire channels, or public playlists.
-   **Flexible Output**: Save results to a shared Google Doc or a local `.docx` file.
-   **Advanced Filtering**: Process all videos or filter by a specific date range, with the option to include or exclude YouTube Shorts.
-   **AI-Powered Transcription**: For videos without built-in captions, the tool uses OpenAI's Whisper model (via Hugging Face) to generate a transcript from the audio.
-   **AI-Powered Formatting**: Optionally use Google's Gemini model to automatically correct grammar, spelling, and punctuation, and to structure the text into clean paragraphs.
-   **Safe API Usage**: Designed to process videos sequentially to respect API rate limits and prevent IP blocks.

## Setup and Installation

Follow these steps to get the application running on your local machine.

### 1. Prerequisites

-   Python 3.8 or higher.
-   [FFmpeg](https://ffmpeg.org/download.html): Required by `yt-dlp` for audio extraction. Please ensure it is installed and accessible in your system's PATH.

### 2. Clone the Repository

Open your terminal and clone the project from GitHub:
```bash
git clone https://github.com/toanmtran/Youtube-Transcript-Extractor.git
cd Youtube-Transcript-Extractor
```

### 3. Set Up a Virtual Environment


```bash
# Create the virtual environment
python -m venv .venv

# Activate the environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 4. Install Dependencies

With the virtual environment active, install all required packages from the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 5. Configure Your Credentials

This project requires API keys and a service account file to function. Your credentials are stored locally.

**a. Set up API Keys:**

-   First, copy the example environment file:
    ```bash
    cp .env.example .env
    ```
-   Next, open the newly created `.env` file and add your secret keys:
    -   `YOUTUBE_DATA_API_KEY`: Get from the [Google Cloud Console](https://console.cloud.google.com/apis/library/youtube.googleapis.com). Enable the **YouTube Data API v3**.
    -   `GOOGLE_AI_API_KEY`: Get from [Google AI Studio](https://aistudio.google.com/app/apikey).
    -   `HF_API_KEY`: Get from your [Hugging Face account settings](https://huggingface.co/settings/tokens).

**b. Set up Google Docs Credentials:**

-   This project uses a Google Service Account to write to Google Docs.
-   Follow the detailed instructions in the `credentials/README.md` file to create a service account, download its JSON key, and place it in the `credentials` folder.

### 6. Run the Application

Once all dependencies and credentials are in place, you can run the application:

```bash
python main.py
```

The tool will guide you through the available options. Enjoy!

## Project Structure

-   `main.py`: The main entry point.
-   `src/cli.py`: Handles all command-line user interaction.
-   `src/config.py`: Manages configuration and loads environment variables.
-   `src/services/`: Contains modules for interacting with external APIs (YouTube, Google AI, Hugging Face) and writing documents.
-   `src/extractors/`: Contains the logic for fetching video data from different sources (channels, playlists).