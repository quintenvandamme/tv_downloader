from .util import get_request, Video

def get_video_from_nieuwsblad(url):
    videos = []
    body = get_request(url,{},False)
    thumbnailUrl = body.split('<meta property="og:image" content="')[1].split('"')[0]    
    videoId = body.split('video-player-')[1].split('\\')[0]
    metadataUrl = 'https://content.tmgvideo.nl/playlist/item=' + videoId + '/playlist.json'
    metadata = get_request(metadataUrl)
    title = metadata["items"][0]["title"]
    description = metadata["items"][0]["description"];
    date = metadata["items"][0]["datecreated"];
    date = date.split('-')
    date = date[2].split(' ')[0] + '-' + date[1] + '-' + date[0] + ' ' + date[2].split(' ')[1]
    streamUrl = metadata['items'][0]['locations']['progressive'][0]['sources'][0]['src']
    fileName = streamUrl.split('/')
    fileName = fileName[len(fileName)-1]
    video = Video(streamUrl, url, title, description, thumbnailUrl, fileName, date)
    videos.append(video)
    return videos