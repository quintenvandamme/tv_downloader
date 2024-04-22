from .util import get_request, Video
import datetime

def getHlnBody(url):
    headers = {'Accept': '*/*','Accept-Language': 'nl,en-US;q=0.7,en;q=0.3','x-mychannels-brand': 'hln','x-mychannels-no-cache': 'false'}
    response = get_request(url,headers,False)
    
    # bypass 500ms delay for google bot auth
    url = response.split("window.location.href = '")[1].split("'")[0]
    response = get_request(url,headers,False)
    return response

def getVideoIds(body):
    ids = []
    
    for line in body.split('\n'):
        if 'data-mychannels-id=' in line:
            videoId = line.split('data-mychannels-id=')[1].split('"')[1]
            if videoId != 'for-you':
                ids.append(videoId)
                
    return ids
        
def get_video(videoId, original_url):
    headers = {'Accept': '*/*','Accept-Language': 'nl,en-US;q=0.7,en;q=0.3','x-mychannels-brand': 'hln','x-mychannels-no-cache': 'false'}
    url = 'https://api.mychannels.world/v1/embed/video/' + videoId + '?statuses[]=published'
    videoInfo = get_request(url,headers)

    title = videoInfo['title']
    description = videoInfo['description']
    thumbnailUrl = videoInfo['image']['baseUrl']
    unixTimeStamp = int(videoInfo['publicationTimestampMs'] / 1000) # convert ms to s
    dt = datetime.datetime.fromtimestamp(unixTimeStamp)
    date = dt.strftime('%d-%m-%Y %H:%M:%S')

    if len(videoInfo['streams']) > 0:
        for stream in videoInfo['streams']:
            if stream['quality'] == 'auto':
                if not 'hlnlive' in stream['url']:
                    if not 'webstream' in stream['url']:
                        fileName = stream['url'].split('/')
                        fileName = fileName[len(fileName)-1].split('.')[0] + '.mp4'
                        streamUrl = stream['url']
                        video = Video(streamUrl, original_url, title, description, thumbnailUrl, fileName, date)
                        return video

def get_video_from_hln(url):
    videos = []
    body = getHlnBody(url)
    videoIds = getVideoIds(body)
    for videoId in videoIds:
        videos.append(get_video(videoId,url))
        
    return videos