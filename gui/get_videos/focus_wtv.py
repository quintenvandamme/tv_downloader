from .util import get_request, Video

def get_metadata_url(body):
    if "'account_id': '" in body:
        accountId = body.split("'account_id': '")[1].split("',")[0]
        item_id = body.split("'item_id': '")[1].split("',")[0]
        return 'https://wfvp.cdn01.rambla.be/play/item/' + accountId + '/' + item_id + '/'

def get_video(metadata_url,url,body):
    json = get_request(metadata_url)

    title = body.split('" property="og:title">')[0].split('<meta content="')
    title = title[len(title)-1]
    description = body.split('" property="og:description">')[0].split('<meta content="')
    description = description[len(description)-1]
    thumbnailUrl = body.split('" property="og:image">')[0].split('<meta content="')
    thumbnailUrl = thumbnailUrl[len(thumbnailUrl)-1]
    streamUrl = 'https://hls-focus-wtv.cdn01.rambla.be/' + json['path'] + '/playlist.m3u8'
    fileName = json['name']
    date = body.split('timestamp="')[1].split('">')[0].split('-')
    date = date[2] + '-' + date[1] + '-' + date[0] + ' ' + date[3] + ':' + date[4] + ':' + date[5]
    
    video = video = Video(streamUrl, url, title, description, thumbnailUrl, fileName, date)
    return  video

def get_video_from_focus_wtv(url):
    videos = []
    body = get_request(url,{},False)
    metadata_url = get_metadata_url(body)
    video = get_video(metadata_url,url,body)
    videos.append(video)
    return videos