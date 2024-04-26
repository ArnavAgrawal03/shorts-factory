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


def create_images(pexels_client, google_client, metadata, save=False, filename="shorts.json"):
    for i, short in enumerate(metadata):
        if short["category"] == "fact":
            metadata[i] = create_images_pexel(pexels_client, short)
        elif short["category"] == "quote":
            metadata[i] = create_images_google(google_client, short)

    if save:
        with open(filename, "w") as fp:
            json.dump(metadata, fp, indent=4)

    return metadata


def create_images_pexel(client, short):
    # for short in metadata:
    photos_dict = make_photo_dict(client, short["thing"])
    image_folder_path = download_images(short["thing"], photos_dict)
    short["image_folder_path"] = image_folder_path

    return short


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


def create_images_google(gis, short):
    path = BASE_PATH / short["thing"]
    google_search_params["q"] = short["thing"]

    gis.search(search_params=google_search_params, path_to_dir=path, width=1080, height=1920)
    short["image_folder_path"] = path

    return short
