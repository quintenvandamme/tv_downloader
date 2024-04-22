from .util import get_request, Video

def get_video_from_ringtv(url):
    videos = []
    body = get_request(url,{},False )
    if 'data-hls-manifest="' in body:
        streamUrl = body.split('data-hls-manifest="')[1].split('"')[0]
        thumbnailUrl = body.split('<meta property="og:image" content="')[1].split('"')[0]
        description = body.split('<meta name="description" content="')[1].split('"')[0]
        title = body.split('<title>')[1].split('</title>')[0].replace(' | Ring','')
        year = body.split('<div class="footer__copyright__info">')[1].split('&copy;')[1].split('&')[0]
        date = '01-01-' + year + ' 01:00:00'
        fileName = streamUrl.split('/')
        fileName = fileName[len(fileName)-2] + '.mp4'
        video = Video(streamUrl, url, title, description, thumbnailUrl, fileName, date)
        videos.append(video)
    return videos