import whisper 
model = whisper.load_model("base")

def audio_to_text(audio_file_path: str) -> str:
    print(audio_file_path)
    result = model.transcribe(audio_file_path)
    
    return result["text"]