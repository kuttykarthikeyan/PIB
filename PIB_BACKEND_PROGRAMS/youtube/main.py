# Start by making sure the `assemblyai` package is installed.
# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Note: Some macOS users might need to use `pip3` instead of `pip`.

# import assemblyai as aai

# # replace with your API token
# aai.settings.api_key = f"aff83dc4cfa84ceeafc04aa722216701"

# # URL of the file to transcribe
# FILE_URL = r"E:\SIH\youtube\trimed_video\full_video.mp4"

# transcriber = aai.Transcriber()
# transcript = transcriber.transcribe(FILE_URL)

# # print(transcript.text)
# print(transcript.export_subtitles_srt())

# import os

# # Set environment variables
# os.environ['GOOGLE_ALERTS_EMAIL'] = 'smartaizxz@gmail.com'
# os.environ['GOOGLE_ALERTS_PASSWORD'] = 'Smartai2003'
# import configparser

# import os
# from google_alerts import GoogleAlerts


# config = configparser.ConfigParser()
# config.read('config.ini')

# email = config['GOOGLE_ALERTS']['email']
# password = config['GOOGLE_ALERTS']['password']

# if email and password:
#     ga = GoogleAlerts(email, password)
#     ga.authenticate()
#     # Continue with the rest of your script
# else:
#     print("Missing credentials. Please set environment variables.")

# import requests
# from bs4 import BeautifulSoup

# # Replace 'url' with the actual URL you want to scrape
# url = 'https://www.careerswave.in/the-times-of-india-pdf-newspaper-download/'
# response = requests.get(url)

# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     # Parse the HTML content of the page
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Find links in the HTML (example: extracting all 'a' tags)
#     links = soup.find_all('tbody')

#     # Print the links

    
    
#     for link in links:
        
#         p = link.find('tr',class_ = 'ninja_table_row_0 nt_row_id_0')
        
#         if p is not None:
#             k = p.get_text()

 
#             print(k[11:])

#         else:
#             print('Failed to retrieve the page. Status code:', response.status_code)

# import gdown

# # Replace the file ID with the one from your Google Drive link
# file_id = "1tsL2ZA0HYt9uAX4HKyUox7svkgC4DXPe"
# # https://drive.google.com/file/d/1tsL2ZA0HYt9uAX4HKyUox7svkgC4DXPe/view?usp=drive_link
# # Replace the output file name
# output_file = "downloaded_file.pdf"

# # Construct the download link
# download_link = f"https://drive.google.com/uc?id={file_id}"

# # Download the file
# gdown.download(download_link, output_file, quiet=False)


# import os
# import urllib.request
 
# linux = os.getenv("HOME")
# outfile = "plink.pdf"
  
# DLFile = urllib.request.urlopen("https://drive.google.com/u/0/uc?id=1tsL2ZA0HYt9uAX4HKyUox7svkgC4DXPe&export=download")
# with open(outfile,'wb') as out:
#     out.write(DLFile.read())

# import requests

# def download_pdf(url, save_path):
#     response = requests.get(url)


# # Replace 'YOUR_PDF_URL' with the actual URL of the PDF file you want to download
# pdf_url = 'https://drive.google.com/u/0/uc?id=1tsL2ZA0HYt9uAX4HKyUox7svkgC4DXPe&export=download'

# # Replace 'path/to/save/file.pdf' with the desired local path where you want to save the PDF
# local_save_path = 'file.pdf'

# download_pdf(pdf_url, local_save_path)


import spacy


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

print(is_government_related("Parliament Winter Session 2023 Highlights: Enquiry Committee formed to probe Lok Sabha security breach"))