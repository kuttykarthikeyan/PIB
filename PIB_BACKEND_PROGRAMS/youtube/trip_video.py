
# def crop_video(input_video_path, start_time,end_time):
#     from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
#     # Trim the video
#     ffmpeg_extract_subclip(input_video_path, start_time, end_time, targetname="trimed_video/output_trimmed_video.mp4")
    
# crop_video("Kannada Actor Rams Car Into Couple , Women Killed - Actor Nagabhushana In Police[00].mp4",0.179,0.179+4.381)

from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def download_youtube_video(youtube_url, output_path):
    # Create a YouTube object
    yt = YouTube(youtube_url)

    # Get the highest resolution stream
    stream = yt.streams.get_highest_resolution()

    # Download the video
    stream.download(output_path=output_path)

def crop_video(input_video_path, start_time, end_time, output_path):
    # Trim the video
    ffmpeg_extract_subclip(input_video_path, start_time, end_time, targetname=output_path)

# YouTube URL
youtube_url = "https://www.youtube.com/watch?v=qD53-RZpTOc"

# Output path for downloaded video
output_video_path = "downloaded_video.mp4"

# Start and end time for trimming (in seconds)
start_time = 0.179
end_time = start_time + 4.381

# Download the YouTube video
download_youtube_video(youtube_url, output_video_path)

# Crop the downloaded video
# crop_video(output_video_path, start_time, end_time, "trimmed_video/output_trimmed_video.mp4")
