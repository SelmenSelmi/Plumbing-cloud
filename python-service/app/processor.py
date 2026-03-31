from __future__ import annotations

import os
import subprocess
import uuid
from pathlib import Path

import cv2
import numpy as np
import whisper

# Keep model in memory to avoid paying initialization cost per request.
WHISPER_MODEL = whisper.load_model(os.getenv("WHISPER_MODEL", "base"))


def _run(command: list[str]) -> None:
    subprocess.run(command, check=True, capture_output=True)


def _extract_audio(input_video: Path, audio_path: Path) -> None:
    _run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(input_video),
            "-vn",
            "-acodec",
            "pcm_s16le",
            "-ar",
            "16000",
            "-ac",
            "1",
            str(audio_path),
        ]
    )


def _write_srt(srt_path: Path, segments: list[dict]) -> None:
    def format_time(value: float) -> str:
        ms = int(value * 1000)
        hours = ms // 3_600_000
        minutes = (ms % 3_600_000) // 60_000
        seconds = (ms % 60_000) // 1000
        millis = ms % 1000
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"

    with srt_path.open("w", encoding="utf-8") as handle:
        for index, segment in enumerate(segments, start=1):
            start = format_time(float(segment["start"]))
            end = format_time(float(segment["end"]))
            text = str(segment["text"]).strip()

            handle.write(f"{index}\n")
            handle.write(f"{start} --> {end}\n")
            handle.write(f"{text}\n\n")


def _detect_face_roi(input_video: Path) -> tuple[int, int, int, int] | None:
    classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    capture = cv2.VideoCapture(str(input_video))

    try:
        ret, frame = capture.read()
        if not ret:
            return None

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) == 0:
            return None

        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        return int(x), int(y), int(w), int(h)
    finally:
        capture.release()


def _detect_motion_roi(input_video: Path) -> tuple[int, int, int, int] | None:
    capture = cv2.VideoCapture(str(input_video))
    first_gray = None
    best_box = None
    best_area = 0

    try:
        while True:
            ret, frame = capture.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if first_gray is None:
                first_gray = gray
                continue

            delta = cv2.absdiff(first_gray, gray)
            thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            contours, _ = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            for contour in contours:
                area = cv2.contourArea(contour)
                if area < 2_000:
                    continue

                x, y, w, h = cv2.boundingRect(contour)
                if area > best_area:
                    best_area = area
                    best_box = (int(x), int(y), int(w), int(h))

        return best_box
    finally:
        capture.release()


def _sanitize_crop(box: tuple[int, int, int, int], width: int, height: int) -> tuple[int, int, int, int]:
    x, y, w, h = box
    x = max(0, min(x, width - 2))
    y = max(0, min(y, height - 2))
    w = max(2, min(w, width - x))
    h = max(2, min(h, height - y))
    return x, y, w, h


def _get_video_dimensions(input_video: Path) -> tuple[int, int]:
    capture = cv2.VideoCapture(str(input_video))
    try:
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if width <= 0 or height <= 0:
            raise RuntimeError("Unable to read video dimensions")
        return width, height
    finally:
        capture.release()


def _render_vertical(
    input_video: Path,
    output_video: Path,
    srt_path: Path,
    face_box: tuple[int, int, int, int],
    motion_box: tuple[int, int, int, int],
) -> None:
    fx, fy, fw, fh = face_box
    mx, my, mw, mh = motion_box

    filter_complex = (
        f"[0:v]crop={fw}:{fh}:{fx}:{fy},scale=1080:720[face];"
        f"[0:v]crop={mw}:{mh}:{mx}:{my},scale=1080:1200[game];"
        f"[game][face]vstack=inputs=2[stacked];"
        f"[stacked]crop=1080:1920:0:0,"
        f"subtitles='{srt_path.as_posix()}':"
        "force_style='FontName=Arial,FontSize=20,PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H00000000,BorderStyle=1,Outline=2,Alignment=2,"
        "MarginV=80,Bold=1'[v]"
    )

    _run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(input_video),
            "-filter_complex",
            filter_complex,
            "-map",
            "[v]",
            "-map",
            "0:a?",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "22",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            str(output_video),
        ]
    )


def process_video(video_path: str) -> str:
    source = Path(video_path)

    if not source.exists():
        raise FileNotFoundError(f"Input video not found: {source}")

    storage_root = source.parents[1]
    processed_dir = storage_root / "videos" / "processed"
    temp_dir = storage_root / "videos" / "tmp"
    processed_dir.mkdir(parents=True, exist_ok=True)
    temp_dir.mkdir(parents=True, exist_ok=True)

    file_id = uuid.uuid4().hex
    audio_path = temp_dir / f"{file_id}.wav"
    srt_path = temp_dir / f"{file_id}.srt"
    output_path = processed_dir / f"{file_id}.mp4"

    _extract_audio(source, audio_path)

    transcript = WHISPER_MODEL.transcribe(str(audio_path), fp16=False)
    segments = transcript.get("segments", [])
    _write_srt(srt_path, segments)

    width, height = _get_video_dimensions(source)

    face_box = _detect_face_roi(source) or (0, 0, width, max(2, int(height * 0.35)))
    motion_box = _detect_motion_roi(source) or (0, int(height * 0.2), width, max(2, int(height * 0.8)))

    face_box = _sanitize_crop(face_box, width, height)
    motion_box = _sanitize_crop(motion_box, width, height)

    _render_vertical(source, output_path, srt_path, face_box, motion_box)

    try:
        audio_path.unlink(missing_ok=True)
        srt_path.unlink(missing_ok=True)
    except OSError:
        pass

    return str(Path("videos") / "processed" / output_path.name)
