from dotenv import load_dotenv
import openai
import os
from pexels_api import API
from item_list import fact_items, quote_people
from text import generate_facts, generate_quotes
from voiceover import create_voiceovers
from image import create_images
from video import create_videos
from google_images_search import GoogleImagesSearch



if __name__ == "__main__":
    load_dotenv()

    openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # things = ["giraffes", "guitars", "pineapples", "dolphins"]
    print("Generating facts")
    facts = generate_facts(openai_client, fact_items, temperature=0.8)

    print("Generating quotes")
    quotes = generate_quotes(openai_client, quote_people, temperature=0.4)

    all_text = facts + quotes

    print("Creating voiceovers")
    short_data = create_voiceovers(openai_client, all_text, voice="echo")

    print("Getting images for fact videos")
    pexels_client = API(os.getenv("PEXELS_API_KEY"))
    google_client = GoogleImagesSearch(os.getenv("GCS_DEVELOPER_KEY"), os.getenv("GCS_CX"))
    short_data = create_images(pexels_client, google_client, short_data)

    print("Creating videos")
    create_videos(short_data)
