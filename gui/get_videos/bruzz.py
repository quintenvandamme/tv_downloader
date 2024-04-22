from .util import get_request, Video

def get_video_from_bruzz(url):
    videos = []
    body = get_request(url,{},False)
    if 'data-item-id="' in body:
        itemId = body.split('data-item-id="')[1].split('"')[0]
        metadata_url = 'https://wfvp.cdn01.rambla.be/play/item/WXv1JD/' + itemId + '/?ref=https%3A%2F%2Fwww.bruzz.be%2F'
        metadata = get_request(metadata_url)
        fileName = metadata['name']
        streamUrl = 'https://hls-bruzz.cdn02.rambla.be/' + metadata['path'] + '/playlist.m3u8'
        date = metadata["created"].split("+")[0].replace('T', ' ')
        date = date.split('-')
        date = date[2].split(' ')[0] + '-' + date[1] + '-' + date[0] + ' ' + date[2].split(' ')[1]
        title = body.split('<meta property="og:title" content="')[1].split('"')[0]
        description = body.split('<meta property="og:description" content="')[1].split('"')[0]
        thumbnailUrl = body.split('<meta property="og:image" content="')[1].split('"')[0]
        video = Video(streamUrl, url, title, description, thumbnailUrl, fileName, date)
        videos.append(video)
    
    return videos