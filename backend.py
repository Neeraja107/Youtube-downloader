from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp
import os

app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cur_dir = os.getcwd()

# Define the Pydantic model for the link
class VideoLink(BaseModel):
    link: str  # Only expect 'link' field as input

@app.post("/download")
async def download_video(data: VideoLink):
    link = data.link  # Extract the link from the request

    youtube_dl_options = {
        "format": "best",
        "outtmpl": os.path.join(cur_dir, f"Bts==(linknode).mp4")
    }

    try:
        with yt_dlp.YoutubeDL(youtube_dl_options) as ydl:
            ydl.download([link])  # Download the video
        return {"status": "download started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
