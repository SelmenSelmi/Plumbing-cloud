# FastAPI Video Processor

This service processes uploaded videos into vertical short-form clips for TikTok/Reels.

## Stack
- FastAPI
- FFmpeg
- OpenCV
- Whisper

## Endpoints
- `POST /process-video`

Request body:

```json
{
  "video_path": "C:/path/to/storage/app/private/videos/originals/input.mp4"
}
```

Response body:

```json
{
  "processed_path": "videos/processed/abcd1234.mp4"
}
```

## Setup

1. Create and activate virtual environment.
2. Install requirements:

```bash
pip install -r requirements.txt
```

3. Ensure FFmpeg is installed and available in PATH.
4. Start service:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```
