import subprocess
import sys
import threading
import progressbar
import os
import os.path
from .constants import *

def checkIfFileExists(outputFile):
    exists = os.path.isfile(outputFile)
    return exists
    

def download_video(url,outputFile):
    if checkIfFileExists(outputFile):
        print(STR_8 % (outputFile,))
    else:
        duration = 0
        out_time = 0
        maxPercentage = 100
        
        progress_bar = progressbar.ProgressBar(widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()], max_value=maxPercentage)
        progress_bar.start()
        
        command = [
            "ffmpeg",
            "-i",
            url,
            "-c",
            "copy",
            outputFile,
            "-progress",
            "-",
            "-nostats"
        ]
        
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
            
        for line in process.stdout:
            if b'Duration: ' in line:
                a = str(line).split('Duration: ')[1].split('.')[0].replace(':','')
                duration = int(a)
            if b'out_time=' in line:
                a = str(line).split('out_time=')[1].split('.')[0].replace(':','')
                out_time = int(a)
                percentage = int((out_time/duration) * 100)
                progress_bar.update(percentage)
            if b'progress=end' in line:
                break;
                
            progress_bar.update(maxPercentage)    
                
        print('\n')
        print(STR_9 % (outputFile,'./'))
        