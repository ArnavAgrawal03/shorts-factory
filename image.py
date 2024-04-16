import requests
import tqdm
import os
from pathlib import Path
import json

PAGE_LIMIT = 10
RESULTS_PER_PAGE = 10
MAX_IMAGES = 12
BASE_PATH = Path(__file__).parent / "images"
RESOLUTION = "original"


def create_images(client, metadata, save=False, filename="shorts.json"):
    for short in metadata:
        photos_dict = make_photo_dict(client, short["thing"])
        image_folder_path = download_images(short["thing"], photos_dict)
        short["image_folder_path"] = image_folder_path

    if save:
        with open(filename, "w") as fp:
            json.dump(metadata, fp, indent=4)

    return metadata


def make_photo_dict(api, query):
    photos_dict, page, counter = {}, 1, 0
    while page < PAGE_LIMIT:
        api.search(query, page=page, results_per_page=RESULTS_PER_PAGE)
        photos = api.get_entries()
        for photo in tqdm.tqdm(photos):
            photos_dict[photo.id] = vars(photo)["_Photo__photo"]
            counter += 1
            if counter >= MAX_IMAGES:
                return photos_dict
            if not api.has_next_page:
                break
            page += 1
    return photos_dict


def download_images(thing, photos_dict):
    path = BASE_PATH / thing
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, f"{thing}.json"), "w") as fout:
        json.dump(photos_dict, fout)
    for val in tqdm.tqdm(photos_dict.values()):
        url = val["src"][RESOLUTION]
        fname = os.path.basename(val["src"]["original"])
        image_path = os.path.join(path, fname)
        if not os.path.isfile(image_path):
            response = requests.get(url, stream=True)
            with open(image_path, "wb") as outfile:
                outfile.write(response.content)
        else:
            # ignore if already downloaded
            print(f"File {image_path} exists")
    return path
