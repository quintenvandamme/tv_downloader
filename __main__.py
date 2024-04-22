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
                print(video)
        else:
            print_error(STR_10)
            break

# test
# https://www.hln.be/buitenland/live-gijzeling-in-nederlands-cafe-voorbij-vier-slachtoffers-vrijgelaten-gijzelnemer-geboeid-door-de-politie~a0dfda52/
# https://www.vrt.be/vrtmax/a-z/vrt-nws-journaal/2024/vrt-nws-journaal-vrt-nws-journaal-laat-20240421/
