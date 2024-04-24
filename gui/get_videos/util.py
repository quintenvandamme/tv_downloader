import requests
import json
import datetime
import os
import sys
import threading
from sys import exit
from io import BytesIO
from .constants import *
from .download import download_video
from PyQt6.QtWidgets import QProgressBar

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    path = relative_path.split('/')
    path = path[len(path)-1]
    return path

def saveFileToPath(fileName):
    return os.path.join(os.getcwd(),fileName)

def print_error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    exit(2)

def post_request(url, data, headers={}):
    try:
        response = requests.post(url, data=json.dumps(data),headers=headers)
        return response.json()
    except:
        print_error(STR_5)

def get_request(url,headers={},isJson=True):
    try:
        response = requests.get(url,headers=headers)
        if isJson == True:
            return response.json()
        else:
            return response.text
    except:
        print_error(STR_5)

def unixTimeToDatetime(unixtime):
    time_offset = 1 #utc +01:00
    date = datetime.datetime.fromtimestamp(unixtime, datetime.timezone(datetime.timedelta(hours=time_offset)))
    datestr = date.strftime("%m-%d-%Y %H:%M:%S")
    return datestr

def getImageData(url):
    try:
        response = requests.get(url)
        img_data = response.content
        return BytesIO(img_data)
    except:
        print_error(STR_5)

class ProgressBar:
    def __init__(self, parent):
        self.progress = 0
        self.progress_bar = QProgressBar()
        parent.layout().addWidget(self.progress_bar)
        self.update(self.progress)
        
    def update(self, progress):
        self.progress = progress
        self.progress_bar.show()
        self.progress_bar.setValue(self.progress)

    def finish(self):
        self.progress = 100
        self.progress_bar.hide()

class Video:
    def __init__(self, streamUrl, originalUrl, title, description, thumbnailUrl, fileName, date):
        self.streamUrl = streamUrl
        self.originalUrl = originalUrl
        self.title = title
        self.description = description
        self.thumbnailUrl = thumbnailUrl
        self.fileName = fileName
        self.date = date
        
    def __str__(self):
        return "streamUrl: " + self.streamUrl + "\nurl: " + self.originalUrl + "\ntitle: " + self.title + "\nthumbnail: " + self.thumbnailUrl + "\nfilename: " + self.fileName + "\ndate: " + self.date
        
    def download(self, guiParent):
        progressBar = ProgressBar(guiParent)
        thread = threading.Thread(target=download_video, args=(self.streamUrl,saveFileToPath(self.fileName), resource_path('./ffmpeg/ffmpeg'),progressBar,))
        thread.start()
        if not thread.is_alive():
            guiParent.layout().removeWidget(progressBar.progress_bar)