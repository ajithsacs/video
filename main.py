import json
import os
import subprocess
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()


@app.get("/api/subtitles/{video_id}")
async def get_subtitles(video_id: str):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        subtitles = [entry["text"] for entry in transcript]
        return JSONResponse(content={"subtitles": subtitles})
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
