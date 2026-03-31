from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .processor import process_video


class ProcessVideoRequest(BaseModel):
    video_path: str = Field(..., description="Absolute path to uploaded source video")


class ProcessVideoResponse(BaseModel):
    processed_path: str


app = FastAPI(title="Video Processor Service", version="1.0.0")


@app.post("/process-video", response_model=ProcessVideoResponse)
def process_video_endpoint(payload: ProcessVideoRequest) -> ProcessVideoResponse:
    try:
        processed_path = process_video(payload.video_path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Video processing failed: {exc}") from exc

    return ProcessVideoResponse(processed_path=processed_path)
