import os
from src.services.youtube_service import YouTubeService
from src.services.ai_services import AIService
from src.services.doc_writers import GoogleDocsWriter, MSWordWriter
from src.extractors.video_extractor import VideoExtractor
from src.extractors.channel_extractor import ChannelExtractor
from src.extractors.playlist_extractor import PlaylistExtractor


class Application:
    """Orchestrates the YouTube transcription process based on user input."""

    def __init__(self):
        self.youtube_service = YouTubeService()
        self.ai_service = AIService()

    def run(self):
        """Main execution loop of the application."""
        while True:
            task, doc_type = self._get_user_choices()

            writer = self._create_writer(doc_type)
            if not writer:
                continue

            if task == '1':  # Single Video
                self._process_single_videos(writer)
            else:  # Channel or Playlist
                extractor = self._create_extractor(task)
                if extractor:
                    self._process_videos_from_extractor(extractor, writer)

            if not self._ask_to_run_again():
                print("\n✨ All done! Hope that was helpful, my dearest! ✨")
                break

    def _get_user_choices(self):
        """Guides the user through selecting the task and document type."""
        print("\n💕 Hello beautiful,\n"
              "Your magical YouTube data helper is here to save the day! "
              "What YouTube adventure shall we embark on today? 🚀\n")
        print("1. Single Video Wormhole 😚🖐️")
        print("2. Channel Conquest Mission 🐟🔱 ")
        print("3. Playlist Treasure Hunt 💎📿\n")

        while True:
            task_option = input("Only 1, 2, or 3 - Choose wisely 😉!\n")
            if task_option in ['1', '2', '3']:
                break
            print("Whoopsie! Invalid option.\n")

        print("\nNow select your expedition vessel:")
        print("1. Google Doc (accessible on all platforms)")
        print("2. MS Word (local file)\n")

        while True:
            doc_option = input("Please enter 1 or 2.\n")
            if doc_option in ['1', '2']:
                break
            print("Oops! Invalid option.\n")

        return task_option, doc_option

    def _create_writer(self, doc_type):
        """Creates a document writer instance."""
        if doc_type == '1':  # Google Docs
            while True:
                doc_link = input("\nEnter a public Google Doc link with editor rights: ")
                try:
                    writer = GoogleDocsWriter(doc_link)
                    return writer
                except ValueError as e:
                    print(f"Error: {e}. Please try again.")

        elif doc_type == '2':  # MS Word
            storage_path = self._get_storage_path()
            return MSWordWriter(storage_path)
        return None

    def _create_extractor(self, task):
        """Creates a video extractor instance."""
        if task == '2':  # Channel
            while True:
                channel_id = input("\nChannel ID can be found at About > Share Channel > Copy channel ID.\n"
                                   "Please enter a YouTube channel ID: ")
                if self.youtube_service.check_channel_id(channel_id):
                    break
                print("Error: Invalid YouTube channel ID\n")
            period = self.youtube_service.get_survey_period()
            include_shorts = self._get_yes_no_response("\nWould you like to capture YouTube shorts? [y/n]\n")
            return ChannelExtractor(self.youtube_service, channel_id, period, include_shorts)

        if task == '3':  # Playlist
            while True:
                playlist_link = input("\nA valid playlist URL starts with https://www.youtube.com/playlist?list=....\n"
                                      "Please enter a Youtube playlist URL: ")
                playlist_id = self.youtube_service.get_playlist_id_from_url(playlist_link)
                if playlist_id and self.youtube_service.check_playlist_id(playlist_id):
                    break
                print("Error: Invalid YouTube playlist URL or ID not found.\n")
            period = self.youtube_service.get_survey_period()
            include_shorts = self._get_yes_no_response("\nWould you like to capture YouTube shorts? [y/n]\n")
            return PlaylistExtractor(self.youtube_service, playlist_id, period, include_shorts)
        return None

    def _process_videos_from_extractor(self, extractor, writer):
        """Processes a collection of videos from a given extractor one by one."""
        print("\nStarting video processing. This may take a while for large channels...")

        use_ai_format = self._get_yes_no_response(
            "\nWould you like our AI buddy to polish the final text (fix grammar, spelling, punctuation)?\n"
            "This may take longer [y/n]: "
        )

        print("\n🛳️ Our vessel is blasting through this YouTube galaxy, capturing every video whisper in its path.\n"
              "👀 Behold our conquered treasures below!\n")

        video_count = 0


        for video_data in extractor.video_generator():
            self._process_single_video(video_data, writer, use_ai_format)
            video_count += 1

        print(f"\n✅ Processed a total of {video_count} videos.")
        writer.save()
        print(f"🎉 {extractor.SUCCESS_MESSAGE}")
        print(f"🟢 Note: {extractor.SORTING_ORDER_NOTE}\n")

    def _process_single_videos(self, writer):
        """Handles the user flow for processing one or more individual videos."""
        videos_to_process = []
        extractor = VideoExtractor(self.youtube_service)

        while True:
            video_url = input("\nEnter a YouTube video URL (or 'done' to finish): ")
            if video_url.lower() == 'done':
                break

            try:
                video_data = extractor.get_video(video_url)
                if video_data:
                    videos_to_process.append(video_data)
                else:
                    print("Could not retrieve video details. It might be private or invalid.")
                    if not self._get_yes_no_response("\nWould you like to skip this video and try another? [y/n]\n"):
                        return
            except Exception as e:
                print(f"An error occurred: {e}")
                if not self._get_yes_no_response("\nWould you like to skip this video and try another? [y/n]\n"):
                    return

        if not videos_to_process:
            print("No videos were added to process.")
            return

        print(f"\n🌎 Total number of videos in our map: {len(videos_to_process)}")
        use_ai_format = self._get_yes_no_response(
            "\nWould you like our AI buddy to polish the final text (fix grammar, spelling, punctuation)?\n"
            "This may take longer [y/n]: "
        )
        print("\n🛳️ Our vessel is blasting through this YouTube galaxy, capturing every video whisper in its path.\n"
              "👀 Behold our conquered treasures below!\n")

        for video_data in videos_to_process:
            self._process_single_video(video_data, writer, use_ai_format)

        writer.save()
        print("🎉 Transcripts kidnapped successfully!!")
        print(
            "🟢 Note: The videos in the doc are sorted from the first video you entered to the last video you entered.\n")

    def _process_single_video(self, video_data, writer, use_ai_format):
        """Core logic to fetch transcript, format, and write a single video."""
        video_title = video_data.get('title', 'Untitled Video')
        video_id = video_data['id']
        print(f"{video_title}\n")

        captions = self.youtube_service.get_transcript(video_id)

        if captions is None:
            print("😯 Bummer! This video doesn't have a built-in transcript.")
            if self._get_yes_no_response(
                    "Would you like our AI buddy to transcribe it for you? This can take a while. [y/n] "):
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                print("🔊 Transcribing audio... please be patient.")
                captions = self.ai_service.transcribe_audio_hf(video_url)

        if not captions:
            captions = "No transcript available for this video."

        if use_ai_format and captions != "No transcript available for this video.":
            print("🤖 AI is polishing the text...")
            formatted_captions = self.ai_service.format_text_gemini(captions)
            if formatted_captions:
                captions = formatted_captions
            else:
                print("AI formatting failed. Using original transcript.")

        try:
            writer.write_video(video_title, captions)
        except Exception as e:
            print(f"Error: Failed to write text for video: {video_title}. Reason: {e}")

    def _get_storage_path(self):
        """Gets a valid directory path from the user for saving files."""
        desktop_paths = [
            os.path.join(os.path.expanduser("~"), "Desktop"),
            os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop"),
        ]
        for path in desktop_paths:
            if os.path.isdir(path):
                print(f"Defaulting to save on your Desktop: {path}")
                return path

        while True:
            custom_path = input("\nCould not find Desktop. Where should we save it? Enter a valid directory path: ")
            if os.path.isdir(custom_path):
                return custom_path
            else:
                print("Uh-oh! That path went off the map. Let's try again!\n")

    def _get_yes_no_response(self, prompt):
        """Helper function to get a 'y' or 'n' answer."""
        while True:
            response = input(prompt).lower()
            if response in ['y', 'n']:
                return response == 'y'
            print("Whoops! Please enter 'y' for Yes or 'n' for No.\n")

    def _ask_to_run_again(self):
        """Asks the user if they want to perform another task."""
        return self._get_yes_no_response("\nWould you like to start another mission? [y/n]\n")