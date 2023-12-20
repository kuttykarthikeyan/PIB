from .models import *
import json
import traceback

def scrap_news_cluster_data_create(data):
    try:
        print("creating headdddd")
        print(type(data))
        news_cluster_head_obj = news_cluster_head()
        data = json.loads(data)
        for key in data:
            setattr(news_cluster_head_obj, key, data[key])
            if key == 'website_data_clustering':
                web_cluster = json.loads(data[key])
            if key == 'youtube_data_clustering':
                youtube_cluster = json.loads(data[key])
        print(news_cluster_head_obj.id,"news cluster head idddddddddddddddddddddddddddddddddddddd")
        news_cluster_head_obj.save()
        news_head_id = news_cluster_head_obj.id
        print(news_head_id,'created headdddddddddddddddd')
        for web_obj in web_cluster:
            print('creating web objjjjjjjj')
            web_object = news_obj()
            for key, value in web_obj.items():
                setattr(web_object, key, value)
            web_object.save()
            obj = news_obj.objects.get(id=web_object.id)
            print(obj)
            obj.source_type=news_obj.website
            obj.clustered = True
            obj.save()
            print('web obj created')
            news_head = news_cluster_head.objects.get(id=news_head_id)
            
            news_head.website_data_cluster_obj.add(obj)
            news_head.save()
            print("website cluster data saved successfully")

        for youtube_obj in youtube_cluster:
            
            youtube_object = news_obj()

            for key, value in youtube_obj.items():
                setattr(youtube_object, key, value)
                
            youtube_object.save()
            obj = news_obj.objects.get(id=youtube_object.id)
            print(obj)
            obj.source_type=news_obj.youtube
            obj.clustered = True
            obj.save()
            news_head = news_cluster_head.objects.get(id=news_head_id)
            news_head.youtube_data_cluster_obj.add(obj)       
            news_head.save()
            print("youtube cluster data saved successfully")
        print("news cluster data saved successfully")
        
    except Exception as e:
        traceback.print_exc()
        print("error occured in news cluster data storing -->"+str(e))