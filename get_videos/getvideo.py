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

def get_videos(url):
    videos = []
    checkedVideos = []
    if validate_url(url):
        if url.startswith("https://www.vrt.be/vrtmax/"):
            videos = get_video_from_vrtmax(url)
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

  
def test():
    #url = 'https://focus-wtv.be/nieuws/miss-belgie-west-vlaamse-finalisten-vallen-niet-in-de-prijzen'
    #url = 'https://www.bruzz.be/actua/politiek/vlaams-minister-van-brussel-regering-blinkt-uit-passiviteit-en-inertie-2024-02-21'
    #url = 'https://www.tvoost.be/nieuws/jan-tratnik-wint-omloop-oliver-naesen-heel-knap-vierde-als-je-vooraf-de-benen-niet-kan-inschatten-is-dit-een-mooi-resultaat-165206'
    #url = 'https://www.tvl.be/nieuws/jongeren-die-voor-het-eerst-stemmen-weten-weinig-of-niets-over-de-verkiezingen-165198'
    #url = 'https://www.robtv.be/nieuws/weekwas-zaterdag-24-februari-165193'
    #url = 'https://www.hln.be/video/productie/we-hebben-de-ram-bij-de-horens-gevat-letterlijk-428950'
    #url = 'https://www.nieuwsblad.be/cnt/dmf20240225_94177728'
    #url = 'https://www.vrt.be/vrtmax/a-z/vrt-nws-journaal/2024/vrt-nws-journaal-vrt-nws-journaal-13u-20240225'
    #url = 'https://www.rtv.be/regionale-sport/wout-van-aert-wil-meteen-scoren-tijdens-openingsweekend'
    #url = 'https://www.vrt.be/vrtnws/nl/kijk/2024/02/25/d7d-oekraine-oorlog-iryna-mudra-gevlucht-met-zoon-nooit-opgeven-/'
    #url = 'https://www.vrt.be/vrtnws/nl/2024/02/26/liveblog-boerenprotest/'
    #url = 'https://www.gva.be/cnt/dmf20240229_96365490'
    #url = 'https://www.ringtv.be/felicitaties-voor-drie-jarigen-die-op-schrikkeldag-jarig-zijn'
    #url = 'https://www.standaard.be/cnt/dmf20231113_92216398'
    #url = 'https://www.vrt.be/vrtnws/nl/2024/02/29/poetin-toespraak-parlement/'
    videos = get_videos(url)
    
    for video in videos:
        print(video)
#test()