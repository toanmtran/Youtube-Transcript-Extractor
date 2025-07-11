from src.extractors.base_extractor import Extractor


class ChannelExtractor(Extractor):
    """Extracts videos from a YouTube channel, one by one."""

    SUCCESS_MESSAGE = "Woohoo! We've gone full ninja on this channel - every transcript is now our prisoner!"
    SORTING_ORDER_NOTE = "The videos in the doc are sorted from newest to oldest publication date."

    def __init__(self, youtube_service, channel_id, period, include_shorts):
        super().__init__(youtube_service, period, include_shorts)
        self.channel_id = channel_id

    def video_generator(self):
        """Yields valid videos from the channel sequentially."""
        for video_data in self.service.fetch_channel_videos_sequentially(self.channel_id):
            if self._is_video_valid(video_data):
                yield video_data