from mutagen.mp3 import MP3
from PIL import Image
import imageio
from moviepy import editor
from pathlib import Path
import os


def create_videos(metadata):
    for short in metadata:
        audio_path = str(short["voiceover_path"].resolve())
        video_path = str((Path(__file__).parent / "videos").resolve())
        images_path = str((short["image_folder_path"]).resolve())

        audio = MP3(audio_path)
        audio_length = audio.info.length

        list_of_images = []
        for image_file in os.listdir(images_path):
            if image_file.endswith(".png") or image_file.endswith(".jpeg"):
                image_path = os.path.join(images_path, image_file)
                image = Image.open(image_path)
                height = image.size[1]
                width = height * 9 / 16
                center = image.size[0]//2
                image = image.crop((center - width//2 , 0, center + width//2, height)).resize(
                    (1080, 1920), Image.LANCZOS
                )
                list_of_images.append(image)

        duration = audio_length / len(list_of_images)
        imageio.mimsave(f"{short['thing']}.gif", list_of_images, fps=1 / duration)

        video = editor.VideoFileClip(f"{short['thing']}.gif")
        audio = editor.AudioFileClip(audio_path)
        final_video = video.set_audio(audio)
        os.chdir(video_path)
        final_video.write_videofile(
            fps=60, codec="libx264", filename=f"{short['thing']}.mp4"
        )
