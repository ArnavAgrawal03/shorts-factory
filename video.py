from mutagen.mp3 import MP3 
from PIL import Image 
import imageio 
from moviepy import editor 
from pathlib import Path 
import os 

def create_videos(metadata):
    for short in metadata:
        audio_path = short['voiceover_path']
        video_path = Path(__file__).parent / "videos"
        images_path = short['image_folder_path']

        audio = MP3(audio_path)
        audio_length = audio.info.length

        list_of_images = [] 
        for image_file in os.listdir(images_path): 
            if image_file.endswith('.png') or image_file.endswith('.jpeg'): 
                image_path = os.path.join(images_path, image_file) 
                image = Image.open(image_path).resize((1080, 1920), Image.ANTIALIAS) 
                list_of_images.append(image)
        
        duration = audio_length/len(list_of_images) 
        imageio.mimsave('images.gif', list_of_images, fps=1/duration)

        video = editor.VideoFileClip("images.gif") 
        audio = editor.AudioFileClip(audio_path) 
        final_video = video.set_audio(audio)
        os.chdir(video_path)
        final_video.write_videofile(fps=60, codec="libx264", filename=f"{short['thing']}.mp4")


