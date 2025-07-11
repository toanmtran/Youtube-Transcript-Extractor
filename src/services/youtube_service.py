import re
import datetime
import isodate
import googleapiclient.discovery
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, CouldNotRetrieveTranscript, NoTranscriptFound
from src.config import YOUTUBE_DATA_API_KEY


class YouTubeService:
    def __init__(self):
        if not YOUTUBE_DATA_API_KEY:
            raise ValueError("YouTube Data API key not found in config.")
        try:
            self.api = googleapiclient.discovery.build('youtube', 'v3', developerKey=YOUTUBE_DATA_API_KEY)
            print("Successfully authenticated with YouTube Data API.")
        except Exception as e:
            raise ConnectionError(f"Failed to authenticate YouTube Data API: {e}")

    def check_channel_id(self, channel_id):
        try:
            request = self.api.channels().list(part="snippet", id=channel_id)
            response = request.execute()
            return 'items' in response and response['items']
        except Exception:
            return False

    def check_playlist_id(self, playlist_id):
        try:
            request = self.api.playlists().list(part="snippet", id=playlist_id)
            response = request.execute()
            return 'items' in response and response['items']
        except Exception:
            return False

    def get_video_details(self, video_id):
        """Fetches details for a single video"""
        try:
            request = self.api.videos().list(part="snippet,contentDetails", id=video_id)
            response = request.execute()
            if not response.get('items'):
                return None
            item = response['items'][0]
            duration_iso = item['contentDetails']['duration']
            duration_sec = isodate.parse_duration(duration_iso).total_seconds()
            return {
                'id': item['id'],
                'title': item['snippet']['title'],
                'published_at': item['snippet']['publishedAt'],
                'duration': duration_sec
            }
        except Exception as e:
            print(f"Error fetching video details for ID {video_id}: {e}")
            return None

    def fetch_channel_videos_sequentially(self, channel_id):
        """
        A generator that yields basic video info (id, title, date) one by one
        """
        page_token = None
        while True:
            request = self.api.search().list(
                part='snippet',
                channelId=channel_id,
                type='video',
                order='date',
                maxResults=50,
                pageToken=page_token
            )
            response = request.execute()
            for item in response.get('items', []):
                yield {
                    'id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'published_at': item['snippet']['publishedAt']
                }
            page_token = response.get('nextPageToken')
            if not page_token:
                break

    def fetch_playlist_videos_sequentially(self, playlist_id):
        """
        A generator that yields basic video info (id, title, date) one by one from a playlist.
        """
        page_token = None
        while True:
            request = self.api.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=page_token
            )
            response = request.execute()
            for item in response.get('items', []):
                if item.get('snippet'):
                    yield {
                        'id': item['snippet']['resourceId']['videoId'],
                        'title': item['snippet']['title'],
                        'published_at': item['snippet'].get('publishedAt')
                    }
            page_token = response.get('nextPageToken')
            if not page_token:
                break


    def get_transcript(self, video_id):
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'vi'])
            return ' '.join([part['text'] for part in transcript_list])
        except (TranscriptsDisabled, CouldNotRetrieveTranscript):
            return None
        except Exception as e:
            # Catch any other unexpected errors.
            print(f"An unexpected error occurred while fetching transcript for video ID {video_id}: {e}")
            return "Error retrieving transcript."

    def get_playlist_id_from_url(self, url):
        match = re.search(r'list=([^&]*)', url)
        return match.group(1) if match else None

    def get_video_id_from_url(self, url):
        patterns = [r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', r'(?:youtu\.be\/|shorts\/)([0-9A-Za-z_-]{11})']
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def get_survey_period(self):
        prompt = ("\nTime to pick your preferred survey period! Options:\n"
                  "- 'all' (for all videos)\n"
                  "- 'b-MM/DD/YYYY' (before a date)\n"
                  "- 'MM/DD/YYYY-e' (after a date)\n"
                  "- 'MM/DD/YYYY-MM/DD/YYYY' (between two dates)\n")

        while True:
            period_str = input(prompt)
            if self._is_valid_period(period_str):
                return period_str
            print('Oops! That period doesn’t look quite right. Give it another shot!')

    def _is_valid_period(self, period):
        if period == 'all': return True
        try:
            if re.fullmatch(r'b-\d{2}/\d{2}/\d{4}', period):
                datetime.datetime.strptime(period[2:], "%m/%d/%Y");
                return True
            if re.fullmatch(r'\d{2}/\d{2}/\d{4}-e', period):
                datetime.datetime.strptime(period[:-2], "%m/%d/%Y");
                return True
            if re.fullmatch(r'\d{2}/\d{2}/\d{4}-\d{2}/\d{2}/\d{4}', period):
                start, end = period.split('-')
                start_date = datetime.datetime.strptime(start, "%m/%d/%Y")
                end_date = datetime.datetime.strptime(end, "%m/%d/%Y")
                return start_date <= end_date
        except ValueError:
            return False
        return False