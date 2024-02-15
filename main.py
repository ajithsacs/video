import json
import os
import subprocess
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from youtube_transcript_api import YouTubeTranscriptApi
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import os
from pydantic import BaseModel
from pyttsx3 import init
from starlette.responses import FileResponse

app = FastAPI()


@app.get("/")
async def demo(video_id: str):
    return "data"


@app.get("/api/subtitles/{video_id}")
async def get_subtitles(video_id: str):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        subtitles = [entry["text"] for entry in transcript]
        paragraph = " ".join(subtitles)

        # response = requests.post("http://localhost:8000/text-to-speech", json={"text":paragraph})
        return paragraph

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/run_subprocess")
async def run_subprocess_view(request: Request):
    body = await request.body()
    x = body.decode()
    json_data = json.loads(x)
    url = json_data["url"]
    try:
        current_directory = os.path.dirname(__file__)
        script_path = os.path.join(current_directory, "process", "frameextracter.py")
        subprocess.run(["python", script_path, url], check=True)

        script_path_2 = os.path.join(current_directory, "process", "videoconverter.py")
        subprocess.run(["python", script_path_2], check=True)

        script_path_3 = os.path.join(current_directory, "process", "mirger.py")
        subprocess.run(["python", script_path_3], check=True)

        return {"message": "Script executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing script: {e}")


@app.get("/get-file/{file_name}")
async def get_file(file_name: str):
    file_path = f"./{file_name}"  # Relative path to the file in the root directory

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, filename=file_name)


class TextToSpeechRequest(BaseModel):
    text: str
    output_filename: str = "output.mp3"  # Optional, default name for audio file


@app.post("/text-to-speech")
async def tts(request: Request, text_to_speech_request: TextToSpeechRequest):
    """Converts text to speech and saves the audio file on the server."""

    try:
        engine = init()
        engine.setProperty("rate", 150)  # Adjust speed as needed
        engine.setProperty("volume", 1)  # Adjust volume as needed

        # Choose a directory for saving the audio file (modify as needed)
        output_path = "process"  # Example path

        engine.save_to_file(
            text_to_speech_request.text,
            os.path.join(output_path, text_to_speech_request.output_filename),
        )
        engine.runAndWait()

        return FileResponse(
            path=os.path.join(output_path, text_to_speech_request.output_filename),
            media_type="audio/mpeg",
            filename=text_to_speech_request.output_filename,
        )

    except Exception as e:
        return {"error": str(e)}
