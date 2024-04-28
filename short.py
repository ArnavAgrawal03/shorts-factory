from pathlib import Path
from dotenv import load_dotenv
from os import getenv
from openai import OpenAI
from google_images_search import GoogleImagesSearch
import json
import random
import csv

# from text import generate_model_response
# from image import create_images_google
# from voiceover import create_voiceover
from video import create_video

STARTER_MESSAGES_GPT = [
    {
        "role": "system",
        "content": "You are generating voiceover text for youtube shorts, "
        + "the voiceover must be 45-55 seconds. We want to keep viewers locked in as long as possible"
        + " your response must be a json object. Have the transcript assigned to the key 'transcript'."
        + " have a list of suggested image searches assigned to the key 'image_searches'.",
    }
]

google_search_params = {
    "q": "...",
    "num": 10,
    "fileType": "jpg|gif|png",
    # "rights": "cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived",
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
        text_model="gpt-4-turbo",
        num_images=15,
        crop=False,
        voice_model="tts-1",
        voice="echo",
        music_path=str((Path(__file__).parent / "music" / "else_paris.mp3").resolve()),
        caption_height=0.5,
        caption_length=20,
    ):

        load_dotenv()

        self.openai_client = OpenAI(api_key=getenv("OPENAI_API_KEY"))
        self.google_client = GoogleImagesSearch(getenv("GCS_DEVELOPER_KEY"), getenv("GCS_CX"))

        self.video_directory = str((Path(__file__).parent / "videos").resolve())

        self.topic = topic
        self.category = category

        self.temperature = temperature
        self.text_model = text_model
        self.num_images = num_images
        self.crop = crop
        self.voice_model = voice_model
        self.voice = voice
        self.caption_height = caption_height
        self.music_path = music_path
        self.caption_length = caption_length

        self.prompt = None
        self.introduction = None
        self._set_category_params()

        self.transcript = None
        self.image_searches = None
        self.image_folder = None
        self.voiceover_path = None
        self.video_path = None

    def generate_short(self, randomize=False):
        if randomize:
            self._randomize_params()
        print("Generating text")
        self._get_text()
        print("Downloading images")
        self._get_images()
        print("Generating voiceover")
        self._get_voiceover()
        print("Creating video")
        self._get_video()
        print("Saving video parameters to metadata file")
        self.update_metadata()

    def _get_text(self):
        new_messages = STARTER_MESSAGES_GPT + [{"role": "user", "content": self.prompt}]

        chat_completion = self.openai_client.chat.completions.create(
            model=self.text_model,
            messages=new_messages,
            temperature=self.temperature,
            response_format={"type": "json_object"},
        )
        json_response = json.loads(chat_completion.choices[0].message.content)

        self.transcript = (
            self.introduction + json_response["transcript"] + " like, comment, and subscribe for more such content!!"
        )

        self.image_searches = json_response["image_searches"]

    def _get_images(self):
        path = BASE_IMAGES_PATH / self.topic
        num_queries = len(self.image_searches)
        images_per_query = (self.num_images // num_queries) + 1

        for image_search in self.image_searches:
            google_search_params["q"] = image_search
            google_search_params["num"] = images_per_query

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
            caption_length=self.caption_length,
        )

    def _set_category_params(self):
        """
        Sets up category specific parameters for the short:
        - introduction
        - prompt
        """
        if self.category == "quote":
            self.prompt = f"Generate 5 interesting quotes by {self.topic}:\n"
            self.introduction = f"Did you know {self.topic} once said: "
        elif self.category == "fact":
            self.prompt = f"Generate 5 interesting trivia facts about {self.topic}:\n"
            self.introduction = f"Did you know these unknown facts about {self.topic}? "
        elif self.category == "fiction_book":
            self.prompt = f"Summarize the plot of the book {self.topic}:\n"
            self.introduction = f"Have you read {self.topic}? Here's a quick summary: "
        elif self.category == "nonfiction_book":
            self.prompt = f"Summarize the key points of the book {self.topic}:\n"
            self.introduction = f"Have you read {self.topic}? Here are the key points it discusses: "

    def _randomize_params(self):
        self.temperature = random.uniform(0.1, 1.0)
        self.text_model = random.choice(["gpt-4-turbo", "gpt-3.5-turbo"])
        self.num_images = random.randint(9, 20)
        self.crop = random.choice([True, False])
        self.voice_model = random.choice(["tts-1", "tts-1-hd"])
        self.voice = random.choice(["alloy", "echo", "fable", "onyx", "nova", "shimmer"])
        self.caption_height = random.uniform(0.3, 0.7)
        self.music_path = str((Path(__file__).parent / "music" / random.choice(["else_paris.mp3"])).resolve())
        self.caption_length = random.randint(8, 20)

    def update_metadata(self):
        metadata_file_path = Path(__file__).parent / "metadata.csv"

        # Check if the metadata file exists, if not, create it and write the header
        if not metadata_file_path.exists():
            with open(metadata_file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        "Topic",
                        "Category",
                        "Temperature",
                        "Text Model",
                        "Num Images",
                        "Crop",
                        "Voice Model",
                        "Voice",
                        "Caption Height",
                        "Music Path",
                        "Caption Length",
                        "Transcript",
                        "Image Searches",
                        "Image Folder",
                        "Voiceover Path",
                        "Video Path",
                    ]
                )

        # Append the metadata of the current YouTube short to the CSV file
        with open(metadata_file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    self.topic,
                    self.category,
                    self.temperature,
                    self.text_model,
                    self.num_images,
                    self.crop,
                    self.voice_model,
                    self.voice,
                    self.caption_height,
                    self.music_path,
                    self.caption_length,
                    self.transcript,
                    json.dumps(self.image_searches),
                    str(self.image_folder),
                    str(self.voiceover_path),
                    str(self.video_path),
                ]
            )
