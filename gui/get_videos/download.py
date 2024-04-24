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
    

def download_video(url,outputFile,ffmpeg_path,progressBar):
    if checkIfFileExists(outputFile):
        print(STR_8 % (outputFile,))
    else:
        duration = 0
        out_time = 0
        
        command = [
            ffmpeg_path,
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
                progressBar.update(percentage)
            if b'progress=end' in line:
                break;
        
        progressBar.finish()
                
        filename = outputFile.split('/')
        filename = filename[len(filename)-1]
        fileDir = outputFile.split(filename)[0]

        print('\n')
        print(STR_9 % (filename,fileDir))
        