from .vrtmax import get_video_from_vrtmax
from .vrtnws import get_video_from_vrtnws_single, get_video_from_vrtnws_multi
from .hln import get_video_from_hln
from .mediahuis import get_video_from_mediahuis
from .focus_wtv import get_video_from_focus_wtv
from .nieuwsblad import get_video_from_nieuwsblad
from .bruzz import get_video_from_bruzz
from .rtv import get_video_from_rtv
from .ringtv import get_video_from_ringtv
from .standaard import get_video_from_standaard
from .constants import *
from .util import print_error

def validate_url(url):
    goodUrl = False
    
    if url.startswith("https://"):
        if len(url) > 8:
            goodUrl = True
            
    return goodUrl

def get_videos(url, settings):
    videos = []
    checkedVideos = []
    if validate_url(url):
        if url.startswith("https://www.vrt.be/vrtmax/"):
            videos = get_video_from_vrtmax(url, settings)
        elif url.startswith("https://www.vrt.be/vrtnws/") and '/kijk/' in url:
            videos = get_video_from_vrtnws_single(url)
        elif url.startswith("https://www.vrt.be/vrtnws/") and not '/kijk/' in url:
            videos = get_video_from_vrtnws_multi(url)
        elif url.startswith("https://www.hln.be/"):
            videos = get_video_from_hln(url)
        elif url.startswith("https://www.bruzz.be/"):
            videos = get_video_from_bruzz(url)
        elif url.startswith("https://www.nieuwsblad.be/"): 
            videos = get_video_from_nieuwsblad(url)
        elif url.startswith("https://www.focus-wtv.be/"):
            videos = get_video_from_focus_wtv(url)
        elif url.startswith("https://www.tvoost.be/") or url.startswith("https://www.tvl.be/") or url.startswith("https://www.robtv.be/") or url.startswith("https://www.gva.be/"):
            videos = get_video_from_mediahuis(url)
        elif url.startswith("https://www.rtv.be/"):
            videos = get_video_from_rtv(url)
        elif url.startswith("https://www.ringtv.be/"):
            videos = get_video_from_ringtv(url)
        elif url.startswith("https://www.standaard.be/"):
            videos = get_video_from_standaard(url)
        else:
            print_error(STR_4)
            
    for video in videos:
        if video != None:
            checkedVideos.append(video)
            
    checkedVideos = list(dict.fromkeys(checkedVideos))        
        
    return checkedVideos
