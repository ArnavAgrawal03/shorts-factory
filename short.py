from pathlib import Path
from dotenv import load_dotenv
from os import getenv
from openai import OpenAI
from google_images_search import GoogleImagesSearch

from text import generate_model_response
from image import create_images_google
from voiceover import create_voiceover
from video import create_video


class Short:
    def __init__(
        self,
        topic,
        category,
        temperature=0.5,
        text_model="gpt-3.5-turbo",
        num_images=10,
        crop=False,
        voice_model="tts-1",
        voice="echo",
        music_path=str((Path(__file__).parent / "music" / "else_paris.mp3").resolve()),
        caption_height=0.5,
    ):

        load_dotenv()

        self.openai_client = OpenAI(api_key=getenv("OPENAI_API_KEY"))
        self.google_client = GoogleImagesSearch(getenv("GCS_DEVELOPER_KEY"), getenv("GCS_CX"))

        self.video_directory = str((Path(__file__).parent / "videos").resolve())
        self.music_path = music_path

        self.topic = topic
        self.category = category

        self.temperature = temperature
        self.text_model = text_model
        self.num_images = num_images
        self.crop = crop
        self.voice_model = voice_model
        self.voice = voice
        self.caption_height = caption_height

        self.prompt = None
        self.transcript = None
        self.image_folder = None
        self.voiceover_path = None
        self.video_path = None

    def _get_text(self):
        response = generate_model_response(
            self.openai_client, self.category, self.topic, self.text_model, self.temperature
        )
        self.transcript = response["response"]
        self.prompt = response["prompt"]

    def _get_images(self):
        self.image_folder = create_images_google(
            gis=self.google_client, thing=self.topic, num_images=self.num_images, crop=self.crop
        )

    def _get_voiceover(self):
        self.voiceover_path = create_voiceover(
            model=self.voice_model, voice=self.voice, client=self.openai_client, thing=self.topic, text=self.transcript
        )

    def _get_video(self):
        self.video_path = create_video(
            voiceover_path=self.voiceover_path,
            image_folder_path=self.image_folder,
            music_path=self.music_path,
            text=self.transcript,
            video_path=self.video_directory,
            topic=self.topic,
            height=self.caption_height,
        )

    def generate_short(self):
        self._get_text()
        self._get_images()
        self._get_voiceover()
        self._get_video()
