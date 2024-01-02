import moviepy.editor as mp
import speech_recognition as sr
from langdetect import detect

def subtitle_maker(headline,SourcePath):
        
        identified_language=detect(headline)
        
        video = mp.VideoFileClip(SourcePath)
        audio_file = video.audio
        audio_file.write_audiofile("audio.wav")

        r = sr.Recognizer()

        with sr.AudioFile("audio.wav") as source:
            data = r.record(source)

        text = r.recognize_google(data,language=identified_language)
        return text
        

subtitle_maker("BREAKING || நள்ளிரவில் நடந்த பயங்கரம்.. வெடித்து சிதறிய பட்டாசு ஆலை விருதுநகரில் நடந்த அதிர்ச்சி..!|","video.mp4")

