import datetime
from abc import ABC, abstractmethod
from src.config import MAX_SHORT_DURATION_SECONDS


class Extractor(ABC):
    """Abstract base class for video data extractors that process items one by one."""

    SUCCESS_MESSAGE = "Processing complete!"
    SORTING_ORDER_NOTE = "Order depends on the source."

    def __init__(self, youtube_service, period='all', include_shorts=True):
        self.service = youtube_service
        self.period = period
        self.include_shorts = include_shorts

    @abstractmethod
    def video_generator(self):
        """
        A generator that yields a single video's data, performing API calls sequentially
        """
        pass

    def _is_video_valid(self, video_data):
        # 1. Check period
        if not self._is_within_period(video_data):
            return False

        # 2. Check shorts
        if not self.include_shorts:
            details = self.service.get_video_details(video_data['id'])
            if not details:
                print(f"Warning: Could not get details for video '{video_data.get('title', 'N/A')}'. Skipping.")
                return False

            # Update video_data with full details for later use
            video_data.update(details)

            if details['duration'] <= MAX_SHORT_DURATION_SECONDS:
                return False

        return True

    def _is_within_period(self, video_data):
        """Filters a single video based on its publication date and the period."""
        if self.period == 'all':
            return True
        try:
            publish_date = datetime.datetime.strptime(
                video_data['published_at'], "%Y-%m-%dT%H:%M:%SZ"
            ).date()

            if self.period.startswith("b-"):
                end_date = datetime.datetime.strptime(self.period[2:], "%m/%d/%Y").date()
                return publish_date <= end_date
            elif self.period.endswith("-e"):
                start_date = datetime.datetime.strptime(self.period[:-2], "%m/%d/%Y").date()
                return publish_date >= start_date
            else:
                start_str, end_str = self.period.split('-')
                start_date = datetime.datetime.strptime(start_str, "%m/%d/%Y").date()
                end_date = datetime.datetime.strptime(end_str, "%m/%d/%Y").date()
                return start_date <= publish_date <= end_date
        except (ValueError, KeyError):
            return True  # Default to including if something is wrong with date