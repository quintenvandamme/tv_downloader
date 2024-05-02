from .util import get_request, Video, unixTimeToDatetime, print_error
from .vrtmax import get_vrtmax_token
from .constants import *

def get_streamUrlAndThumbnail(videoId, pubId, vrtmaxToken,guiParent):
    url = 'https://media-services-public.vrt.be/media-aggregator/v2/media-items/' + pubId + '$' + videoId + '?vrtPlayerToken=' + vrtmaxToken + '&client=vrtnieuws'
    a = get_request(url,{})
    mpegUrl = a['targetUrls'][1]['url']
    streamUrl = mpegUrl.split('?')[0]
    if not 'nodrm' in streamUrl:
        print_error(STR_6,guiParent)
    thumbnailUrl = a['posterImageUrl']
    return streamUrl, thumbnailUrl

def get_video_from_vrtnws_single(url,guiParent):
    videos = []
    body = get_request(url,{},False)
    title = body.split('<meta itemprop="name" content="')[1].split('"')[0]
    description = body.split('<meta name="description" content="')[1].split('"')[0]
    if 'data-video-id="' in body and 'data-publication-id="' in body:
        videoId = body.split('data-video-id="')[1].split('"')[0]
        pubId = body.split('data-publication-id="')[1].split('"')[0]
        vrtmaxToken = get_vrtmax_token()
        streamUrlAndThumbnail = get_streamUrlAndThumbnail(videoId,pubId,vrtmaxToken,guiParent)
        streamUrl = streamUrlAndThumbnail[0]
        thumbnailUrl = streamUrlAndThumbnail[1]
        fileName = videoId + '.mp4'
        date = body.split('"publishDate":"')[1].split('"')[0].split('-')
        date = date[2] + '-' + date[1] + '-' + date[0] + ' 01:00:00'
        video = Video(streamUrl, url, title, description, thumbnailUrl, fileName, date)
        videos.append(video)
        return videos

def get_video_from_vrtnws_multi(url,guiParent):
    videos = []
    body = get_request(url,{},False)
    
    # a token is valid for a certain time so we don't have to generate one for every video
    vrtmaxToken = get_vrtmax_token() 
    
    # getting the time of the page since videos on a normal page don't contain date's
    unixTime = int(int(body.split('"page_id":"')[1].split('"')[0])/1000) # get unix time in seconds
    date = unixTimeToDatetime(unixTime)
    
    lines = body.split('\n')
    for line in lines:
        if 'data-video-id="' in line and 'data-publication-id="' in line:
            videoId = line.split('data-video-id="')[1].split('"')[0]
            pubId = line.split('data-publication-id="')[1].split('"')[0]          
            streamUrlAndThumbnail = get_streamUrlAndThumbnail(videoId,pubId,vrtmaxToken,guiParent)
            streamUrl = streamUrlAndThumbnail[0]
            thumbnailUrl = streamUrlAndThumbnail[1]
            title = line.split('data-title="')[1].split('"')[0]
            fileName = videoId + '.mp4'
            description = ''
            video = Video(streamUrl, url, title, description, thumbnailUrl, fileName, date)
            videos.append(video)
            
    return videos