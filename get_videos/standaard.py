from .util import get_request, Video

def get_video_from_standaard(url):
    videos = []
    body = get_request(url,{},False)
    lines = body.split('\n')
    for line in lines:
        if '"videoId":"' in line:
            videoId = body.split('"videoId":"')[1].split('"')[0]
            description = body.split('"description":"')[1].split('"')[0]
            jsonUrl = 'https://content.mediahuisvideo.be/playlist/item=' + videoId + '/playlist.json'
            json = get_request(jsonUrl)
            title = json['items'][0]['title']
            thumbnailUrl = json['items'][0]['poster']
            streamUrl = json['items'][0]['locations']['progressive'][0]['sources'][0]['src']
            fileName = streamUrl.split('/')
            fileName = fileName[len(fileName)-1]
            date = json['items'][0]['datecreated'].split('-')
            date = date[2].split(' ')[0] + '-' + date[1] + '-' + date[0] + ' ' + date[2].split(' ')[1]
            video = Video(streamUrl, url, title, description, thumbnailUrl, fileName, date)
            videos.append(video)
            
    return videos