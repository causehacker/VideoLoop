# Video Looper

A simple Python utility to create looped versions of video files by concatenating a video with itself multiple times.

## Features

- Loop a video a specific number of times
- Loop a video to achieve a target duration
- Preserves original video quality (no re-encoding)
- Fast processing using FFmpeg's concat demuxer

## Requirements

- Python 3.6+
- FFmpeg (with ffprobe)

## Installation

1. Ensure you have Python 3.6 or higher installed
2. Install FFmpeg:
   - **macOS**: `brew install ffmpeg`
   - **Ubuntu/Debian**: `sudo apt install ffmpeg`
   - **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html) and add to PATH
3. Download the `video_looper.py` script

## Usage

```bash
python video_looper.py <input_video_path> <loop_count_or_duration>
```

### Examples

```bash
python video_looper.py input.mp4 5
```


### Parameters

- `input_video_path`: Path to the input video file
- `loop_count_or_duration`: Either:
  - A positive integer (e.g., `3`) to loop the video that many times
  - A time in `mm:ss` format (e.g., `1:30`) to loop the video to achieve approximately that duration

### Examples

Loop a video 3 times:

```bash
python video_looper.py input.mp4 3
```

Loop a video to approximately 1 minute 30 seconds:

```bash
python video_looper.py input.mp4 1:30
```


## Output

The script creates a new video file in the same directory as the input file, with "_loop" appended to the filename.

For example, if the input file is `video.mp4`, the output file will be `video_loop.mp4`.

## How It Works

1. If a target duration is specified, the script:
   - Gets the duration of the input video using ffprobe
   - Calculates how many loops are needed to achieve the target duration
   - Rounds to the nearest whole number of loops

2. The script creates a temporary file listing the input video multiple times

3. FFmpeg's concat demuxer is used to concatenate the videos without re-encoding

4. The temporary file is cleaned up after processing

## Troubleshooting

- **FFmpeg not found**: Ensure FFmpeg is installed and in your system PATH
- **Permission denied**: Ensure you have write permissions in the directory
- **Invalid time format**: Use `mm:ss` format (e.g., `1:30`) or a positive integer

## License

This project is open source and available under the MIT License.