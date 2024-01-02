import moviepy.editor as mp
import time
import speech_recognition as sr

# Load the video
video = mp.AudioFileClip(r'E:\PIB_project_folder\SIH\youtube\video\full_video.mp4')

# Extract the audio from the video

video.write_audiofile("geeksforgeeks.wav")

# Initialize recognizer
r = sr.Recognizer()

start_time = time.time()

# Load the audio file
with sr.AudioFile("geeksforgeeks.wav") as source:
	data = r.record(source)
 
# Convert speech to text
text = r.recognize_google(data,language='en-IN')

# Print the text
print("\nThe resultant text from video is: \n")
print(text)
end_time = time.time()

print(end_time - start_time)

