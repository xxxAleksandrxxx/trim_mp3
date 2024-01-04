from fastapi import FastAPI, UploadFile, File
from pydub import AudioSegment
from io import BytesIO

app = FastAPI()

def trim_audio(input_audio, start_time, end_time):
    audio = AudioSegment.from_file(input_audio, format="mp3")
    trimmed_audio = audio[start_time:end_time]  # Assuming start_time and end_time are in miliseconds
    return trimmed_audio

@app.post("/trim-mp3")
async def trim_mp3(file: UploadFile = File(...), start_time: int = 0, end_time: int = 0):
    try:
        # Read the uploaded file into memory
        audio_content = BytesIO(file.file.read())

        # Trim the audio in memory
        trimmed_audio = trim_audio(audio_content, start_time, end_time)

        # Save the trimmed audio to memory
        trimmed_content = BytesIO()
        trimmed_audio.export(trimmed_content, format="mp3")

        return {"message": "File processed successfully", "processed_file": trimmed_content.getvalue()}
    except Exception as e:
        return {"error": str(e)}
