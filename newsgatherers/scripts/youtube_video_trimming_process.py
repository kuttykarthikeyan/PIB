import os
import pandas as pd
import json,shutil
from langdetect import detect
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import ffmpeg 
import subprocess    
analyzer = SentimentIntensityAnalyzer()
def sentiment_analysis(descriptions):
    global analyzer
    list_results = []
    for text in descriptions:
        results = {}
        sen_list = ['POSITIVE','NEGATIVE','NEUTRAL']
        sentiment_score = analyzer.polarity_scores(text)
        sentiment_intensity = sentiment_score['compound']

        if sentiment_intensity >= 0.3:
            sentiment = "POSITIVE"
        elif sentiment_intensity <= -0.5:
            sentiment = "NEGATIVE"
        else:
            sentiment = "NEUTRAL"
            
        sen_list.remove(sentiment)
        
        sentiment_intensity = abs(sentiment_intensity)
        
        results['SENTIMENT_LABEL'] = sentiment
        results[sentiment] = round(sentiment_intensity * 100,2)
        results[sen_list[0]] = 0
        results[sen_list[1]] = 0
        
        list_results.append(results)
        
        
    return list_results


googletrans_translator = Translator()
def language_translation(input_string,target_lag):
    global googletrans_translator
    detect_language = detect(input_string)
    if detect_language != 'en':
        language_list = {'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'azerbaijani': 'az', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-cn', 'chinese (traditional)': 'zh-tw', 'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dutch': 'nl', 'english': 'en', 'esperanto': 'eo', 'estonian': 'et', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el', 'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'he', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'korean': 'ko', 'kurdish (kurmanji)': 'ku', 'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lithuanian': 'lt', 'luxembourgish': 'lb', 'macedonian': 'mk', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr', 'mongolian': 'mn', 'myanmar (burmese)': 'my', 'nepali': 'ne', 'norwegian': 'no', 'odia': 'or', 'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 'scots gaelic': 'gd', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'telugu': 'te', 'thai': 'th', 'turkish': 'tr', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'}
        googletrans_result = googletrans_translator.translate(input_string,src= "auto", dest= language_list[target_lag])
        return googletrans_result.text
    else:
        return input_string

def delete_contents_of_directory(directory_path):
    try:
        # Remove all files and subdirectories
        shutil.rmtree(directory_path)
        
        # Recreate an empty directory
        os.mkdir(directory_path)
        
        print(f"Contents of '{directory_path}' deleted successfully.")
    except Exception as e:
        print(f"Error: {e}")

# from moviepy.video.io.VideoFileClip import VideoFileClip

# def crop_video(input_video_path, start_time,end_time,output_file):
#     from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
#     # Trim the video
#     ffmpeg_extract_subclip(input_video_path, start_time, end_time, targetname="videos/" + output_file)
        
def crop_video(input_video_path, start_time, end_time, output_file):
    from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
    output_directory = "newsgatherers/static/"

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Construct the full output path
    output_path = os.path.join(output_directory, output_file)

    try:
        # Trim the video
        ffmpeg_extract_subclip(input_video_path, start_time, end_time, targetname=output_path)
        print(f"Conversion successful: {output_path}")
    except Exception as e:
        print(f"Error during conversion: {e}")
    

url = "https://www.youtube.com/watch?v=R-eZz44vLns"

def youtube_video_trimming_process(video_url):
    
    from youtube_transcript_api import YouTubeTranscriptApi
    import pandas as pd
    
    indian_languages_interchanged = {"Bangla": "bn", "Bhojpuri": "bho", "Gujarati": "gu", "Hindi": "hi", "Kannada": "kn", "Malayalam": "ml", "Marathi": "mr", "Nepali": "ne", "Odia": "or", "Punjabi": "pa", "Sanskrit": "sa", "Tamil": "ta", "Telugu": "te", "Urdu": "ur"}
    all_languages = {'Afrikaans': 'af', 'Akan': 'ak', 'Albanian': 'sq', 'Amharic': 'am', 'Arabic': 'ar', 'Armenian': 'hy', 'Assamese': 'as', 'Aymara': 'ay', 'Azerbaijani': 'az', 'Bangla': 'bn', 'Basque': 'eu', 'Belarusian': 'be', 'Bhojpuri': 'bho', 'Bosnian': 'bs', 'Bulgarian': 'bg', 'Burmese': 'my', 'Catalan': 'ca', 'Cebuano': 'ceb', 'Chinese (Simplified)': 'zh-Hans', 'Chinese (Traditional)': 'zh-Hant', 'Corsican': 'co', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da', 'Divehi': 'dv', 'Dutch': 'nl', 'English': 'en', 'Esperanto': 'eo', 'Estonian': 'et', 'Ewe': 'ee', 'Filipino': 'fil', 'Finnish': 'fi', 'French': 'fr', 'Galician': 'gl', 'Ganda': 'lg', 'Georgian': 'ka', 'German': 'de', 'Greek': 'el', 'Guarani': 'gn', 'Gujarati': 'gu', 'Haitian Creole': 'ht', 'Hausa': 'ha', 'Hawaiian': 'haw', 'Hebrew': 'iw', 'Hindi': 'hi', 'Hmong': 'hmn', 'Hungarian': 'hu', 'Icelandic': 'is', 'Igbo': 'ig', 'Indonesian': 'id', 'Irish': 'ga', 'Italian': 'it', 'Japanese': 'ja', 'Javanese': 'jv', 'Kannada': 'kn', 'Kazakh': 'kk', 'Khmer': 'km', 'Kinyarwanda': 'rw', 'Korean': 'ko', 'Krio': 'kri', 'Kurdish': 'ku', 'Kyrgyz': 'ky', 'Lao': 'lo', 'Latin': 'la', 'Latvian': 'lv', 'Lingala': 'ln', 'Lithuanian': 'lt', 'Luxembourgish': 'lb', 'Macedonian': 'mk', 'Malagasy': 'mg', 'Malay': 'ms', 'Malayalam': 'ml', 'Maltese': 'mt', 'Māori': 'mi', 'Marathi': 'mr', 'Mongolian': 'mn', 'Nepali': 'ne', 'Northern Sotho': 'nso', 'Norwegian': 'no', 'Nyanja': 'ny', 'Odia': 'or', 'Oromo': 'om', 'Pashto': 'ps', 'Persian': 'fa', 'Polish': 'pl', 'Portuguese': 'pt', 'Punjabi': 'pa', 'Quechua': 'qu', 'Romanian': 'ro', 'Russian': 'ru', 'Samoan': 'sm', 'Sanskrit': 'sa', 'Scottish Gaelic': 'gd', 'Serbian': 'sr', 'Shona': 'sn', 'Sindhi': 'sd', 'Sinhala': 'si', 'Slovak': 'sk', 'Slovenian': 'sl', 'Somali': 'so', 'Southern Sotho': 'st', 'Spanish': 'es', 'Sundanese': 'su', 'Swahili': 'sw', 'Swedish': 'sv', 'Tajik': 'tg', 'Tamil': 'ta', 'Tatar': 'tt', 'Telugu': 'te', 'Thai': 'th', 'Tigrinya': 'ti', 'Tsonga': 'ts', 'Turkish': 'tr', 'Turkmen': 'tk', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uyghur': 'ug', 'Uzbek': 'uz', 'Vietnamese': 'vi', 'Welsh': 'cy', 'Western Frisian': 'fy', 'Xhosa': 'xh', 'Yiddish': 'yi', 'Yoruba': 'yo', 'Zulu': 'zu'}

    video_id = video_url.split("=")[1]
    # retrieve the available transcripts
    
    
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # iterate over all available transcripts
        for transcript in transcript_list:
            # whether it has been manually created or generated by YouTube
            transcript.video_id,
            detected_lan = transcript.language_code,
            
            # whether this transcript can be translated or not
            transcript.is_translatable
            
            actual_subtitle = transcript.fetch()   
            
        subtitle_dict = {}
        subtitle_list = [ i["text"] for i in actual_subtitle]
    
        
        subtitle_dict["subtitle"] = subtitle_list
        subtitle_dict["start_time"] = [ i["start"]  for i in actual_subtitle]
        subtitle_dict["end_time"] = [ i["start"] + i["duration"] for i in  actual_subtitle]


        sentiment_analysis_result = sentiment_analysis( [ language_translation(i,'english') for i in  list(subtitle_dict["subtitle"]) ])    
    
        subtitle_dict['POSITIVE'] = [ i['POSITIVE'] for i in sentiment_analysis_result]
        subtitle_dict['NEUTRAL'] = [ i['NEUTRAL'] for i in sentiment_analysis_result]
        subtitle_dict['NEGATIVE'] = [ i['NEGATIVE'] for i in sentiment_analysis_result]
        subtitle_dict['SENTIMENT_LABEL'] = [ i['SENTIMENT_LABEL']  for i in sentiment_analysis_result]

        video_analysis_dataframe = pd.DataFrame(subtitle_dict)
        print(video_analysis_dataframe)
        video_analysis_dataframe.to_csv("youtube_single_video_data.csv")
        json = video_analysis_dataframe.loc[:,['subtitle','SENTIMENT_LABEL']].to_json()
        
        video_analysis_dataframe_neg = video_analysis_dataframe.query('SENTIMENT_LABEL == "NEGATIVE"')
        print("ooef",len(video_analysis_dataframe_neg))
        print(video_analysis_dataframe_neg)
        print(type(video_analysis_dataframe_neg))
        
        
        if len(video_analysis_dataframe) != 0:
            return video_analysis_dataframe_neg,json
        else:
            return pd.DataFrame()
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Subtitles are disabled for this video")
        

def spliting_negative_clip(url,id):   

    from tqdm import tqdm
    global r
    import yt_dlp

    r,_ = youtube_video_trimming_process(url)
    print(len(r))

    
    ydl_opts = {
        'age_limit': 18,
        'outtmpl': 'downloaded_youtube_video/downloaded_video.mp4' 
    }
    

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    # output_video_path = "downloaded_youtube_video/downloaded_video.mp4"
    # input_video_path ="downloaded_youtube_video/downloaded_video.mp4.webm"
    # ffmpeg_command = [
    #     'ffmpeg',
    #     '-i', input_video_path,
    #     '-c:v', 'copy',
    #     '-c:a', 'aac',
    #     '-strict', 'experimental',
    #     output_video_path
    # ]
    list_trim_video = list(zip(r["start_time"],r["end_time"]))
    # try:
        
    #     subprocess.run(ffmpeg_command, check=True)
    #     print("Conversion successful")
    #     os.remove("downloaded_youtube_video/downloaded_video.mp4.webm")
    # except subprocess.CalledProcessError as e:
    #     print(f"Error during conversion: {e}")
    videos = []
    if len(list_trim_video) != 0:
        
        for i,j in tqdm(enumerate(list_trim_video)):
            
            crop_video("downloaded_youtube_video/downloaded_video.mp4",start_time=j[0],end_time=j[1],output_file="negative_"+str(id)+ "_" +str(i+1)+".mp4")
            video_filename = "negative_"+str(id)+"_"+str(i+1)+".mp4"
            videos.append(video_filename)
            print(video_filename)
        crop_video("downloaded_youtube_video/downloaded_video.mp4",start_time=0,end_time=list(r["end_time"])[-1],output_file=str(id)+ "_" +"full_video.mp4")

        os.remove("downloaded_youtube_video/downloaded_video.mp4")
        print("successfully!!!!!!!!!")
        return json.dumps(videos)