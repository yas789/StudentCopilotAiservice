import os
import tempfile
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional

import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from moviepy.editor import VideoFileClip
from typing import Optional
from fastapi import BackgroundTasks

app = FastAPI()

    

@app.get("/")
def read_root():
    return {"Hello": "World"}





##Video TOOOO AUDIO:
@app.post("/extract-audio/")
async def extract_audio_from_video(
    background_tasks: BackgroundTasks,
    video: UploadFile = File(...),
    output_format: str = "mp3",
    start_time: Optional[float] = None,
    duration: Optional[float] = None
):
    # Read video buffer
    video_buffer = await video.read()

    # Create a temporary file to store the videohost 
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(video_buffer)
        temp_video_path = temp_video.name

    try:
        # Load the video file
        video_clip = VideoFileClip(temp_video_path)

        # Extract audio
        audio = video_clip.audio

        # Apply options if provided
        if start_time is not None:
            audio = audio.subclip(start_time)
        if duration is not None:
            audio = audio.subclip(0, duration)

        # Create a temporary file for the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{output_format}") as temp_audio:
            temp_audio_path = temp_audio.name

        # Write audio to file
        audio.write_audiofile(temp_audio_path)

        # Close the video to release resources
        video_clip.close()

        # Schedule background task to clean up the temporary files after the response is sent
        background_tasks.add_task(os.unlink, temp_video_path)
        background_tasks.add_task(os.unlink, temp_audio_path)

        # Return the audio file
        return FileResponse(temp_audio_path, media_type=f"audio/{output_format}", filename=f"extracted_audio.{output_format}")

    except Exception as e:
        # Clean up the temp video file in case of error
        os.unlink(temp_video_path)
        raise HTTPException(status_code=500, detail=str(e))
    
    