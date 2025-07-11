class VideoExtractor:
    """
    A simple utility to retrieve and validate data for a single YouTube video URL.
    """

    def __init__(self, youtube_service):
        self.service = youtube_service

    def get_video(self, video_url):
        """Retrieves and validates data for a single video URL."""
        video_id = self.service.get_video_id_from_url(video_url)
        if not video_id:
            print("Error: Could not extract a valid Video ID from the URL.")
            return None

        return self.service.get_video_details(video_id)