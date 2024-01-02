import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_video_paylist_results():
    options = Options()
    # running selenium in headless mode
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.youtube.com/results?search_query=dnb playlist')

    youtube_playlist = []

    for result in driver.find_elements_by_xpath('//*[@id="contents"]/ytd-playlist-renderer'):
        playlist_title = result.find_element_by_css_selector('#video-title').text
        playlist_link = result.find_element_by_css_selector('.style-scope ytd-playlist-renderer a').get_attribute('href')
        channel_name = result.find_element_by_css_selector('#channel-name').text
        video_count = result.find_element_by_css_selector('#overlays > ytd-thumbnail-overlay-side-panel-renderer > yt-formatted-string').text

        youtube_playlist.append({
            'title': playlist_title,
            'link': playlist_link,
            'count': video_count,
            'channel': channel_name,
        })

    print(json.dumps(youtube_playlist, indent=2, ensure_ascii=False))

get_video_paylist_results()