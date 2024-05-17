from dotenv import load_dotenv
import openai
import os
from pexels_api import API
from item_list import fact_items, quote_people, fiction_books, nonfiction_books, titles
from old_files.text import generate_facts, generate_quotes
from old_files.voiceover import create_voiceovers
from old_files.image import create_images
from video import create_videos
from google_images_search import GoogleImagesSearch

from short import Short


def main1():
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

    print("Getting images for videos")
    pexels_client = API(os.getenv("PEXELS_API_KEY"))
    google_client = GoogleImagesSearch(os.getenv("GCS_DEVELOPER_KEY"), os.getenv("GCS_CX"))
    short_data = create_images(pexels_client, google_client, short_data)

    print("Creating videos")
    create_videos(short_data)


def main2():
    shorts = []

    for fact in fact_items:
        shorts.append(Short(topic=fact, category="fact"))

    for person in quote_people:
        shorts.append(Short(topic=person, category="quote"))

    for book in fiction_books:
        shorts.append(Short(topic=book, category="fiction_book"))

    for book in nonfiction_books:
        shorts.append(Short(topic=book, category="nonfiction_book"))

    for title in titles:
        shorts.append(Short(topic=title, category="title"))

    for short in shorts:
        print(f"Generating short for {short.topic}")
        short.generate_short(randomize=True)


if __name__ == "__main__":
    # main1()
    main2()
