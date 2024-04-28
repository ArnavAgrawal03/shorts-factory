from pathlib import Path
from dotenv import load_dotenv
from os import getenv
from openai import OpenAI
from google_images_search import GoogleImagesSearch

# from text import generate_model_response
# from image import create_images_google
# from voiceover import create_voiceover
from video import create_video

STARTER_MESSAGES_GPT = [
    {
        "role": "system",
        "content": "You are generating voiceover text for youtube shorts, "
        + "the voiceover must be 20-35 seconds. It must also be sensational in nature",
    }
]

google_search_params = {
    "q": "...",
    "num": 10,
    "fileType": "jpg|gif|png",
    "rights": "cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived",
    # "safe": "active",
    # "imgSize": "large",  # 'huge|icon|large|medium|small|xlarge|xxlarge|imgSizeUndefined', ##
    # 'imgDominantColor': 'black|blue|brown|gray|green|orange|pink|purple|red|teal|white|yellow|imgDominantColorUndefined',
    # 'imgColorType': 'color|gray|mono|trans|imgColorTypeUndefined' ##
    # 'imgType': 'clipart|face|lineart|stock|photo|animated|imgTypeUndefined', ##
}

BASE_IMAGES_PATH = Path(__file__).parent / "images"


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

    def generate_short(self):
        self._get_text()
        self._get_images()
        self._get_voiceover()
        self._get_video()

    def _get_text(self):
        introduction, prompt = self._get_intro_and_prompt()
        new_messages = STARTER_MESSAGES_GPT + [{"role": "user", "content": prompt}]

        chat_completion = self.openai_client.chat.completions.create(
            model=self.text_model, messages=new_messages, temperature=self.temperature
        )

        self.prompt = prompt
        self.transcript = (
            introduction + chat_completion.choices[0].message.content + " subscribe for more quotes and facts!!"
        )

    def _get_images(self):
        path = BASE_IMAGES_PATH / self.topic
        google_search_params["q"] = self.topic
        google_search_params["num"] = self.num_images

        if self.crop:
            self.google_client.search(search_params=google_search_params, path_to_dir=path, width=1080, height=1920)
        else:
            self.google_client.search(search_params=google_search_params, path_to_dir=path)

        self.image_folder = path

    def _get_voiceover(self):
        speech_file_path = Path(__file__).parent / "voiceovers" / f"{self.topic}.mp3"
        response = self.openai_client.audio.speech.create(
            model=self.voice_model, voice=self.voice, input=self.transcript
        )
        response.stream_to_file(speech_file_path)

        self.voiceover_path = speech_file_path

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

    def _get_intro_and_prompt(self):
        if self.category == "quote":
            prompt = f"Generate 3 interesting quotes by {self.topic}:\n"
            introduction = f"Did you know {self.topic} once said: "
        elif self.category == "fact":
            prompt = f"Generate 3 interesting trivia facts about {self.topic}:\n"
            introduction = f"Did you know these 3 unknown facts about {self.topic}? "

        return introduction, prompt
