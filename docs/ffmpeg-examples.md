# FFmpeg Command Examples

These commands match the processing format used by the microservice.

## 1. Extract Audio

```bash
ffmpeg -y -i input.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav
```

## 2. Facecam Crop and Scale (Top Region)

```bash
ffmpeg -y -i input.mp4 -filter:v "crop=640:360:0:0,scale=1080:720" facecam_top.mp4
```

## 3. Gameplay Crop and Scale (Bottom Region)

```bash
ffmpeg -y -i input.mp4 -filter:v "crop=1920:1080:0:200,scale=1080:1200" gameplay_bottom.mp4
```

## 4. Stack Facecam + Gameplay to 9:16

```bash
ffmpeg -y -i gameplay_bottom.mp4 -i facecam_top.mp4 \
-filter_complex "[0:v][1:v]vstack=inputs=2,crop=1080:1920:0:0" \
-c:v libx264 -pix_fmt yuv420p stacked_vertical.mp4
```

## 5. Burn Captions with Bold Style

```bash
ffmpeg -y -i stacked_vertical.mp4 \
-vf "subtitles=captions.srt:force_style='FontName=Arial,FontSize=20,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Alignment=2,MarginV=80,Bold=1'" \
-c:v libx264 -crf 22 -preset medium -c:a aac -b:a 192k final_1080x1920.mp4
```

## 6. Final Export Requirements

- Resolution: `1080x1920`
- Codec: `H.264` (`libx264`)
- Pixel format: `yuv420p`
- Container: `MP4`
- Audio: `AAC`
