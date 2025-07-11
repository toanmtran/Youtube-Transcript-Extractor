from src.extractors.base_extractor import Extractor


class PlaylistExtractor(Extractor):
    """Extracts videos from a YouTube playlist, one by one."""

    SUCCESS_MESSAGE = "Playlist transcript heist complete! We've stolen more words than a literary bandit!"
    SORTING_ORDER_NOTE = "The videos in the doc are sorted from newest to oldest publication date."

    def __init__(self, youtube_service, playlist_id, period, include_shorts):
        super().__init__(youtube_service, period, include_shorts)
        self.playlist_id = playlist_id

    def video_generator(self):
        """Yields valid videos from the playlist sequentially."""
        for video_data in self.service.fetch_playlist_videos_sequentially(self.playlist_id):
            if self._is_video_valid(video_data):
                yield video_data