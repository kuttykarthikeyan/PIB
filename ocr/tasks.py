import fitz,os
from tqdm import tqdm
from ultralytics import YOLO
import cv2
import re
import shutil
from pathlib import Path
from googletrans import Translator
import json
import pandas as pd
import spacy
import easyocr
from textblob import TextBlob
from nltk.tokenize import sent_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from . models import *
import datetime


language_selection_dict = { "english_newspapers" : 'en' ,'telugu_newspapers' : 'te','hindi_newspapers':'hi' }


def delete_contents_of_directory(directory_path):
    try:
        # Remove all files and subdirectories
        shutil.rmtree(directory_path)
       
        # Recreate an empty directory
        os.mkdir(directory_path)
       
        print(f"Contents of '{directory_path}' deleted successfully.")
    except Exception as e:
        print(f"Error: {e}")


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

def is_government_related(news_text):
    # List of government-related keywords
    government_keywords = [
        'government', 'governance', 'public service', 'public office', 'public sector', 'public policy',
        'political', 'politics', 'politician', 'democracy', 'election', 'political party', 'citizen', 'civic',
        'state', 'national', 'federal', 'municipal', 'local government', 'public official', 'public servant',
        'executive', 'administration', 'president', 'prime minister', 'cabinet', 'minister', 'secretary',
        'commissioner', 'governor', 'mayor', 'official', 'authority', 'policy maker', 'bureaucrat', 'regulator',
        'legislator', 'lawmaker', 'parliamentarian', 'representative', 'senator', 'congressman', 'congresswoman',
        'assemblyman', 'assemblywoman', 'diplomat', 'embassy', 'consulate', 'diplomacy', 'ambassador', 'foreign affairs',
        'international relations', 'treaty', 'summit', 'conference', 'convention', 'protocol', 'trade agreement',
        'bilateral', 'multilateral', 'trilateral', 'executive order', 'presidential decree', 'government agency',
        'department', 'ministry', 'bureau', 'office', 'commission', 'board', 'authority', 'committee', 'task force',
        'regulatory body', 'ombudsman', 'civil service', 'treasury', 'finance', 'budget', 'taxation', 'education',
        'health', 'public health', 'defense', 'national defense', 'justice', 'judiciary', 'law enforcement',
        'homeland security', 'border control', 'immigration', 'customs', 'transportation', 'infrastructure',
        'agriculture', 'environment', 'natural resources', 'energy', 'power', 'labor', 'employment', 'unemployment',
        'housing', 'urban development', 'rural development', 'commerce', 'trade', 'business', 'industry', 'technology',
        'information', 'communication', 'telecommunications', 'internet', 'interior', 'veterans affairs',
        'social services', 'welfare', 'social security', 'culture', 'arts', 'heritage', 'tourism', 'sports', 'recreation',
        'science', 'research', 'development', 'innovation', 'sustainability', 'climate change', 'foreign aid', 'aid',
        'human rights', 'civil liberties', 'constitution', 'constitutional', 'policy analysis', 'government program',
        'government initiative', 'public initiative', 'public project', 'government expenditure', 'public spending',
        'government revenue', 'public funds', 'government debt', 'public debt', 'public finance', 'political science'
    ]
   
    nlp = spacy.load("en_core_web_sm")
 
    doc = nlp(news_text)
 
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PERSON", "GPE"]:
            return True
 
    for token in doc:
        if token.text.lower() in government_keywords:
            return True
 
    return False
 

def image_to_text_OCR(image_path):
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    text = pytesseract.image_to_string(image=image_path)
    return text
 

def ocr_easy(image_path,lang):
    reader = easyocr.Reader([lang])  
    results = reader.readtext(image_path)
   
    telugu_text = []
    for detection in results:
        text = detection[1]
        telugu_text.append(text)
 
    return "".join(telugu_text)



def clean_text(text,lang):
    global language_selection_dict
    df = {}
    # Remove unwanted characters and extra spaces
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    remove_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    blob = TextBlob(remove_text)
    cleaned_text = str(blob.correct())
    print("!!!!!!!!!!!!!!!@@@@@@@@@!!!!!!!!!!!!!!!!!!!!",text)
    if is_government_related(cleaned_text):
        print("is_government_related",cleaned_text)
        sentences_sent_tokenize = sent_tokenize(cleaned_text)
        sentiment_list = sentiment_analysis(cleaned_text)
        print(sentiment_list)
        print("!!!!!!22222222223333333333332222222222!!!!!!!",sentences_sent_tokenize)
        sentences = language_translation(cleaned_text,lang)
        print(sentences)
        df["full_text"] = cleaned_text
        df["sentances"] = sentences_sent_tokenize
        sen_result_list = [ i['SENTIMENT_LABEL'] for i in sentiment_list]
        df['SENTIMENT_ANALYSIS_RESULT'] = sen_result_list
        df['POSITIVE'] = [ i['POSITIVE'] for i in sentiment_list]
        df['NEUTRAL'] = [ i['NEUTRAL'] for i in sentiment_list]
        df['NEGATIVE'] = [ i['NEGATIVE'] for i in sentiment_list]
        df['positive_sentances'] = [ i for i,j in zip(sentences_sent_tokenize,sen_result_list) if j == "POSITIVE" ]
        df['negative_sentances'] = [ i for i,j in zip(sentences_sent_tokenize,sen_result_list) if j == "NEGATIVE" ]
        df['neutral_sentances'] = [ i for i,j in zip(sentences_sent_tokenize,sen_result_list) if j == "NEUTRAL" ]

        return df
    else:
        return False


def e_print_function(newspaper_lang):
   
    global language_selection_dict
 
    model = YOLO(r"./model_ocr/model_article_only.pt")
 
 
    # folder_path = Path("pdfs/" + newspaper_lang)
    # files_name_folder = [f.name for f in folder_path.iterdir() if f.is_file() ]
    papers = DailyOCR.objects.filter(languauge=newspaper_lang,date=datetime.datetime.now().date())
 
    for paper in papers:
       
        doc = fitz.open(paper.file.path)
        # os.makedirs("OCR_results/" + file_name + "_pdf", exist_ok=True)
       
        # dict_data = {}
        pages_dict = {}
       
        for id, page in enumerate(doc):
           
            pix = page.get_pixmap(matrix=fitz.Identity, dpi=None, colorspace=fitz.csRGB, clip=None, annots=True)
           
            page_name = str(paper.id) + "-%i.jpg" % page.number
            pdf_img_path  = "media/ocr/" + page_name
            pix.save(pdf_img_path)
            input_image = cv2.imread(pdf_img_path)
 
            results = model.predict(source=pdf_img_path, conf=0.20,iou=0.8)
            results_image = results[0].plot()
           
            # os.makedirs("OCR_results/" + file_name + "_pdf" + "/page_"+str(id+1),exist_ok=True)
            # cv2.imwrite("OCR_results/" + file_name + "_pdf" + "/page_"+str(id+1)+"/full_image.jpg", results_image)
            cv2.imwrite("/media/ocr/" +"/page_"+str(id+1)+".jpg", results_image)

            page_obj = Page.objects.create(ocr_object=paper,file = "/media/ocr/" +"/page_"+str(id+1)+".jpg",page_number = page.number)

 
            boxes = results[0].boxes.numpy().xyxy
            classes = results[0].boxes.numpy().cls
           
            img_num = 1
            art_num = 1
            art_dict = {}
           
            for b, c in zip(boxes, classes):
                if c == 0:
                    x1, y1 = b[0], b[1]  # Top-left corner
                    x2, y2 = b[2], b[3]  # Bottom-right corner
                    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                    cropped_image = input_image[y1:y2, x1:x2]
                   
                    if newspaper_lang == 'english_newspapers':
                        image_to_text = image_to_text_OCR(cropped_image)
                       
                    if newspaper_lang == 'telugu_newspapers':
                        image_to_text = ocr_easy(cropped_image,language_selection_dict[newspaper_lang])
                        image_to_text = language_translation(image_to_text,'english')
                        print("**********************",image_to_text)
                   
                    if newspaper_lang == 'hindi_newspapers':
                        image_to_text = ocr_easy(cropped_image,language_selection_dict[newspaper_lang])
                        image_to_text = language_translation(image_to_text,'english')
                       
                    # print(newspaper_lang.split("_")[0])
                    analysis_text = clean_text(image_to_text,newspaper_lang.split("_")[0])
                    print(analysis_text)
                   
                    if analysis_text != False:
                        print("trueeee")
                        art_dict["article_" + str(art_num)] = analysis_text
                        cv2.imwrite("/media/ocr/" + "page_"+str(id+1)+"_article_" + str(art_num) + ".png", cropped_image)
                        OCRResult.objects.create(page=page_obj,name=str(art_num),file="/media/ocr/" + "page_"+str(id+1)+"_article_" + str(art_num) + ".png")
                        art_num += 1
           
            pages_dict["page_"+str(id+1)] = art_dict
            art_num = 1      
            img_num = 1
            art_dict = {}
           
           
           
 
        # dict_data[paper.name] = pages_dict
        # pages_dict = {}    
           
        # json_string = json.dumps(dict_data, indent=2)
        paper.json_result = pages_dict
        paper.save()
           
    print("Successfully completed " + newspaper_lang +" !!!!!!!!!!!!!!!!!!!!!!")



@shared_task
def perform_ocr():
    import threading
 
 
    # Define the languages
    languages = ['english_newspapers','telugu_newspapers', 'hindi_newspapers']
    
    # for i in languages:
    #     os.makedirs("images_from_pdf/" + i, exist_ok=True)
    
    # Create a thread for each language
    threads = []
    
    for lang in languages:
        thread = threading.Thread(target=e_print_function, args=(lang,))
        threads.append(thread)
    
    
    # Start all the threads
    for thread in threads:
        thread.start()
    
    # Wait for all threads to finish
    for thread in threads:
        thread.join()

