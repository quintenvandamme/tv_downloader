from .util import get_request, Video

def get_video_from_mediahuis(url):
    videos = []
    body = get_request(url,{},False)
    videoId = ''
    
    if '"videoId":"' in body: # gva.be
        videoId = body.split('"videoId":"')[1].split('"')[0]
    if 'videoId: "' in body:
        videoId = body.split('videoId: "')[1].split('"')[0]
    if 'data-video-embed-id="' in body:
        videoId = body.split('data-video-embed-id="')[1].split('"')[0]
    
    if videoId != '':
        jsonUrl = 'https://content.tmgvideo.nl/playlist/item=' + videoId + '/playlist.json'
        json = get_request(jsonUrl)
        title = json['items'][0]['title']
        description = json['items'][0]['description']
        thumbnailUrl = json['items'][0]['poster']
        streamUrl = json['items'][0]['locations']['progressive'][0]['sources'][0]['src']
        fileName = streamUrl.split('/')
        fileName = fileName[len(fileName)-1]
        date = json['items'][0]['datecreated'].split('-')
        date = date[2].split(' ')[0] + '-' + date[1] + '-' + date[0] + ' ' + date[2].split(' ')[1]
        video = Video(streamUrl, url, title, description, thumbnailUrl, fileName, date)
        videos.append(video)
    
    return videos