import requests
import json
import datetime
import os
import sys
from io import BytesIO
from .constants import *
from .download import download_video


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

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
        
    def download(self):
        download_video(self.streamUrl,self.fileName)