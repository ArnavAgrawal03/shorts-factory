from pathlib import Path

def create_voiceovers(client, facts, model="tts-1", voice="echo"):
    for fact in facts:
        text, thing = fact["response"], fact["thing"]
        speech_file_path = Path(__file__).parent / "voiceovers" / f"{thing}.mp3"
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )
        response.stream_to_file(speech_file_path)
        fact["voiceover_path"] = speech_file_path
    return facts # now this is metadata, but stored in the same dict as "facts"