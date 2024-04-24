from mutagen.mp3 import MP3
from PIL import Image
import imageio
from moviepy import editor
from pathlib import Path
import os
import random


def create_videos(metadata):
    video_path = str((Path(__file__).parent / "videos").resolve())
    music_path = str((Path(__file__).parent / "music" / "else_paris.mp3").resolve())

    for short in metadata:
        audio_path = str(short["voiceover_path"].resolve())
        images_path = str((short["image_folder_path"]).resolve())
        # subtitles = sensationalize(short["response"])

        audio_length, composite_audio = create_audio(audio_path, music_path)
        video = create_slideshow(audio_length, short, images_path)
        txt_clip = create_subtitle_clips(audio_length, chunk(short["response"])).set_position(("center", 0.7), relative=True)
        # txt_clip = create_captions(subtitles, video.duration)

        video = editor.CompositeVideoClip([video, txt_clip], size=video.size)

        final_video = video.set_audio(composite_audio)
        os.chdir(video_path)
        final_video.write_videofile(
            fps=60, codec="libx264", filename=f"{short['thing']}.mp4"
        )


def create_audio(audio_path, music_path):
    audio = MP3(audio_path)
    audio_length = audio.info.length

    audio = editor.AudioFileClip(audio_path)
    music = editor.AudioFileClip(music_path).subclip(0, audio_length).volumex(0.2)
    composite_audio = editor.CompositeAudioClip([audio, music])

    return audio_length, composite_audio

def create_slideshow(audio_length, short, images_path):
    list_of_images = []
    for image_file in os.listdir(images_path):
        if image_file.endswith(".jpeg"):  # image_file.endswith(".png") or
            image_path = os.path.join(images_path, image_file)
            image = Image.open(image_path)
            height = image.size[1]
            width = height * 9 / 16
            center = image.size[0] // 2
            image = image.crop(
                (center - width // 2, 0, center + width // 2, height)
            ).resize((1080, 1920), Image.LANCZOS)
            list_of_images.append(image)

    duration = audio_length / len(list_of_images)
    imageio.mimsave(f"{short['thing']}.gif", list_of_images, fps=1 / duration)
    return editor.VideoFileClip(f"{short['thing']}.gif")


def chunk(text, char_limit=25):
    text, new_text = text.split(), []
    line, i, current_chars = [], 0, 0
    while i < len(text):
        shout = random.choice([True, False, False, False, False, False])
        word = text[i].upper() if shout else text[i]

        if current_chars + len(word) <= char_limit:
            line.append(word)
            current_chars += len(word) + 1
            i += 1
        else:
            new_text.append(" ".join(line))
            line = []
            current_chars = 0
    new_text.append(" ".join(line))
    return new_text


def create_subtitle_clips(audio_length, chunks):
    time_per_line = audio_length / len(chunks)
    clips = []
    for line in chunks:
        txt_clip = editor.TextClip(
            line,
            fontsize=60,
            color="white",
            stroke_color="black",
            stroke_width=4,
            size=(1080 * 3 / 4, None),
            bg_color="transparent",
            font="Arial-Bold"
        )
        clips.append(txt_clip.set_position(("center", "bottom")).set_duration(time_per_line))
    return editor.concatenate_videoclips(clips, method="compose")


# old functions:


# def create_captions(subtitles, video_length):
#     txt_clip = editor.TextClip(
#         subtitles,
#         fontsize=60,
#         color="white",
#         # stroke_color="black",
#         # stroke_width=1.5,
#         size=(1080 * 3 / 4, None),
#         bg_color="black",
#     )
#     return txt_clip.set_pos(("center", "bottom")).set_duration(video_length)


# def sensationalize(text):
#     new_text = []
#     for word in text.split():
#         shout = random.choice([True, False, False, False, False])
#         new_text.append(word.upper() if shout else word)
#     return " ".join(new_text)