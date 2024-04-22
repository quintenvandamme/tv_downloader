import sys
from get_videos import get_videos
from get_videos.constants import *

def handelArgs():
    args = sys.argv[1:]
    args_len = len(args)
    
    for arg in args:
        if '-v' == arg or '--version' == arg and args_len == 1:
            print(f'Version {VERSION} - {VERSION_DATE}')

def test():
    url = 'https://www.hln.be/buitenland/live-gijzeling-in-nederlands-cafe-voorbij-vier-slachtoffers-vrijgelaten-gijzelnemer-geboeid-door-de-politie~a0dfda52/'
    videos = get_videos(url)
    for video in videos:
        print(video)
        #video.download()
        
test()