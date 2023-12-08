# def admin_dashboard(request):
#         try:    
#             latest_news = News.objects.all()

#             for news_object in latest_news:
                
#                 render_latest_news.delay(news_object.id)

#         except Exception as e:
#             print(str(e))
#         return render(request, 'admin_dashboard.html')