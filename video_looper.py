import subprocess
import sys
import os
import re
from datetime import datetime

def get_video_duration(video_path):
    """Get duration of video in seconds using ffprobe"""
    command = [
        'ffprobe', 
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return float(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error getting video duration: {e}")
        sys.exit(1)

def parse_time_str(time_str):
    """Convert mm:ss format to seconds"""
    try:
        # Try mm:ss format
        if ':' in time_str:
            time_obj = datetime.strptime(time_str, '%M:%S')
            return time_obj.minute * 60 + time_obj.second
        # Try numeric format (loop count)
        else:
            count = int(time_str)
            if count < 1:
                raise ValueError("Loop count must be positive")
            return None  # Return None to indicate this is a loop count
    except ValueError as e:
        print(f"Error: Invalid time format. Use mm:ss or a positive number")
        sys.exit(1)

def loop_video(input_video, loop_spec):
    # Get the directory and filename from the input path
    directory = os.path.dirname(input_video)
    filename = os.path.basename(input_video)
    
    # Create output filename
    name, ext = os.path.splitext(filename)
    output_video = os.path.join(directory, f"{name}_loop{ext}")
    
    # Determine loop count based on input specification
    if isinstance(loop_spec, str):
        target_seconds = parse_time_str(loop_spec)
        if target_seconds is None:  # This means loop_spec was a count
            loop_count = int(loop_spec)
        else:
            # Calculate required loops based on target duration
            video_duration = get_video_duration(input_video)
            loop_count = max(1, round(target_seconds / video_duration))
            print(f"Video duration: {video_duration:.2f}s")
            print(f"Target duration: {target_seconds}s")
            print(f"Will loop {loop_count} times to achieve approximately {loop_count * video_duration:.2f}s")
    
    # Create a temporary file listing the input video multiple times
    temp_list_file = os.path.join(directory, 'temp_list.txt')
    with open(temp_list_file, 'w') as f:
        for _ in range(loop_count):
            f.write(f"file '{input_video}'\n")
    
    # Construct the ffmpeg command using the concat demuxer
    command = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', temp_list_file,
        '-c', 'copy',
        '-y',
        output_video
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"Successfully created looped video: {output_video}")
        os.remove(temp_list_file)
    except subprocess.CalledProcessError as e:
        print(f"Error creating looped video: {e}")
        if os.path.exists(temp_list_file):
            os.remove(temp_list_file)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python video_looper.py <input_video_path> <loop_count_or_duration>")
        print("Examples:")
        print("  python video_looper.py input.mp4 3     # Loop 3 times")
        print("  python video_looper.py input.mp4 1:30  # Loop to achieve ~1 min 30 sec")
        sys.exit(1)
    
    input_video = sys.argv[1]
    loop_spec = sys.argv[2]
    
    loop_video(input_video, loop_spec) 