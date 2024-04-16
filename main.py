from dotenv import load_dotenv
load_dotenv()

import openai, os
from pexels_api import API
from item_list import random_items
from text import generate_facts
from voiceover import create_voiceovers
from image import create_images
from video import create_videos


if __name__ == "__main__":
    
    openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # things = ["giraffes", "guitars", "pineapples", "dolphins"]
    print("Generating facts")
    facts = generate_facts(openai_client, random_items, temperature=0.7)
    
    print("Creating voiceovers")
    short_data = create_voiceovers(openai_client, facts) 
    
    print("Getting images for video")
    pexels_client = API(os.getenv("PEXELS_API_KEY"))
    short_data = create_images(pexels_client, short_data)

    print("Creating videos")
    create_videos(short_data)


