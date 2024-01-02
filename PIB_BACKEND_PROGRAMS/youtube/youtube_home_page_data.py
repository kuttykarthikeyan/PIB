import os
import json
import pandas as pd
import googleapiclient.discovery

API_KEY = 'AIzaSyBGPcCzN_moSe6i0f8_BxB2Moa7nGd-Aww'

def search_youtube(api_key, keyword, max_results=5, return_json=False):
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

    search_response = youtube.search().list(
        q=keyword,
        type='video',
        part='id,snippet',
        maxResults=max_results
    ).execute()

    videos = search_response.get('items', [])
    video_details = []
    if videos:
        for video in videos:
            print(video)
            video_id = video['id']['videoId']
            title = video['snippet']['title']
            channel = video['snippet']['channelTitle']
            publish = video['snippet']['publishedAt']
            thumbnail_url = video['snippet']['thumbnails']['default']['url']
            description = video['snippet']['description']

            video_details.append({
                'title': title,
                'description': description,
                'source_name': channel,
                'published_date': publish,
                'url': f'https://www.youtube.com/watch?v={video_id}',
                'thumbnail_url': thumbnail_url,
            })



    if return_json:
        return pd.DataFrame(video_details)
    else:
        return video_details



search_keyword = "modi "
max_results = 1

result = search_youtube(API_KEY, search_keyword, max_results, return_json=True)
print(result)