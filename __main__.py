import sys
from get_videos import get_videos
from get_videos.constants import *
from get_videos.util import print_error

def handelArgs():
    args = sys.argv[1:]
    args_len = len(args)
    
    for arg in args:
        if '-v' == arg or '--version' == arg and args_len == 1:
            print(f'Version {VERSION} - {VERSION_DATE}')
        elif '-i' == arg and args_len == 2:
            url = args[1]
            videos = get_videos(url)
            for video in videos:
                video.download()
        else:
            print_error(STR_10)

handelArgs()

# test
# https://www.hln.be/buitenland/live-gijzeling-in-nederlands-cafe-voorbij-vier-slachtoffers-vrijgelaten-gijzelnemer-geboeid-door-de-politie~a0dfda52/
# https://www.vrt.be/vrtmax/a-z/vrt-nws-journaal/2024/vrt-nws-journaal-vrt-nws-journaal-laat-20240421/
# https://focus-wtv.be/nieuws/miss-belgie-west-vlaamse-finalisten-vallen-niet-in-de-prijzen
# https://www.bruzz.be/actua/politiek/vlaams-minister-van-brussel-regering-blinkt-uit-passiviteit-en-inertie-2024-02-21
# https://www.tvoost.be/nieuws/jan-tratnik-wint-omloop-oliver-naesen-heel-knap-vierde-als-je-vooraf-de-benen-niet-kan-inschatten-is-dit-een-mooi-resultaat-165206
# https://www.tvl.be/nieuws/jongeren-die-voor-het-eerst-stemmen-weten-weinig-of-niets-over-de-verkiezingen-165198
# https://www.robtv.be/nieuws/weekwas-zaterdag-24-februari-165193
# https://www.hln.be/video/productie/we-hebben-de-ram-bij-de-horens-gevat-letterlijk-428950
# https://www.nieuwsblad.be/cnt/dmf20240225_94177728
# https://www.vrt.be/vrtmax/a-z/vrt-nws-journaal/2024/vrt-nws-journaal-vrt-nws-journaal-13u-20240225
# https://www.rtv.be/regionale-sport/wout-van-aert-wil-meteen-scoren-tijdens-openingsweekend
# https://www.vrt.be/vrtnws/nl/kijk/2024/02/25/d7d-oekraine-oorlog-iryna-mudra-gevlucht-met-zoon-nooit-opgeven-/
# https://www.vrt.be/vrtnws/nl/2024/02/26/liveblog-boerenprotest/
# https://www.gva.be/cnt/dmf20240229_96365490
# https://www.ringtv.be/felicitaties-voor-drie-jarigen-die-op-schrikkeldag-jarig-zijn
# https://www.standaard.be/cnt/dmf20231113_92216398
# https://www.vrt.be/vrtnws/nl/2024/02/29/poetin-toespraak-parlement/