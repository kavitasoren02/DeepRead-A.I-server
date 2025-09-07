from  gtts import gTTS
import os
import re

audio_dir = os.path.join(os.path.dirname(__file__), "..", "audio")
os.makedirs(audio_dir, exist_ok=True)
def text_to_audio(text: str):

    clean_text = re.sub(r"\s+", " ", re.sub(r"[\*\#\n]", " ", text)).strip()
    filename = f"summary_{len(os.listdir(audio_dir)) + 1}.mp3"
    output_path = os.path.join(audio_dir, filename)

    tts = gTTS(clean_text)
    tts.save(output_path)

    print(f"Audio saved to {output_path}")
    return filename