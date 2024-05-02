from .util import get_request, Video, unixTimeToDatetime, print_error
from .vrtmax import get_vrtmax_token
from .constants import *
import json

def get_streamUrl(mediaReference,guiParent):
    vrtmaxToken = get_vrtmax_token()
    url = 'https://media-services-public.vrt.be/media-aggregator/v2/media-items/' + mediaReference + '?vrtPlayerToken=' + vrtmaxToken + '&client=vrtnieuws'
    a = get_request(url,{})
    mpegUrl = a['targetUrls'][1]['url']
    streamUrl = mpegUrl.split('?')[0]
    if not 'nodrm' in streamUrl:
        print_error(STR_6,guiParent)
    return streamUrl

def get_video_from_nwsnwsnws(url,guiParent):
    videos = []

    body = get_request(url,{},False)
    try:
        data = body.split('<script id="__NEXT_DATA__" type="application/json">')[1].split('</script>')[0]
        data = json.loads(data)
        
        thumbnailUrl = data['props']['pageProps']['data']['compositions'][0]['compositions'][0]['action']['image']['url']
        mediaReference = data['props']['pageProps']['data']['compositions'][0]['compositions'][0]['action']['mediaReference']
        streamUrl = get_streamUrl(mediaReference,guiParent)
        title = data['props']['pageProps']['data']['compositions'][0]['compositions'][1]['title']['text']
        description = data['props']['pageProps']['data']['compositions'][0]['compositions'][2]['text']['html']
        date = data['props']['pageProps']['data']['compositions'][0]['compositions'][2]['metadata'][0]['timestamp']
        date = unixTimeToDatetime(int(date/1000))
        fileName = mediaReference.split('$')[1] + '.mp4'

        video = Video(streamUrl, url, title, description, thumbnailUrl, fileName, date)
        videos.append(video)
    except:
        pass

    return videos