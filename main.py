from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()


@app.get("/api/subtitles/{video_id}")
async def get_subtitles(video_id: str):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        subtitles = [entry['text'] for entry in transcript]
        return JSONResponse(content={'subtitles': subtitles})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
