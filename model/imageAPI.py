# -*- coding: utf-8 -*-
import os
import sys
import urllib.request
import json
import subprocess
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from view import AccessSettings

class ImageProvider:
    """
    This object makes search requests to pixabay with the key of the user
    """
    def __init__(self, word):
        self.word = word
        self.key = AccessSettings.getPixabayKey()
        myURL = "https://pixabay.com/api/?key=" + self.key + "&q=" + self.word.replace(' ', '+') + "&image_type=photo"
        myURL = ''.join(i for i in myURL if ord(i)<128)
        with urllib.request.urlopen(myURL) as url:
            self.data = json.loads(url.read().decode())
        self.provisionNumber = 0
        self.hitNumber = self.data["total"]
        self.hitNumber = min(20, self.hitNumber)
    def getFirstImage(self):
        imageURL = self.data["hits"][0]["webformatURL"][8:]
        tmp_dir = os.path.join(BASE_DIR, "images", "tmp")
        return_code = subprocess.call("wget -P " + tmp_dir + " " + imageURL, shell=True)
        return "images/tmp/" + imageURL.split('/')[-1]
    def getImageBatch(self):
        """
        Downloads images in search results 5 at a time into /images/tmp directory
        """
        paths = list()
        for i in range(self.provisionNumber, self.provisionNumber+5):
            if i == self.hitNumber:
                break
            imageURL = self.data["hits"][i]["webformatURL"][8:]
            tmp_dir = os.path.join(BASE_DIR, "images", "tmp")
            if not os.path.exists(tmp_dir): os.mkdir(tmp_dir)
            return_code = subprocess.call("wget -P " + tmp_dir + " " + imageURL, shell=True)
            # do smthg when return code is bad
            paths.append("images/tmp/" + imageURL.split('/')[-1])
        self.provisionNumber += len(paths)
        return paths
    def keepImage(self, path):
        subprocess.call("mv " + path + " " + os.path.join(BASE_DIR, "images/"), shell=True)
        return os.path.join("images", path.split('/')[-1])
    def cleanUp(self):
        """
        empties the /images/tmp directory of all its content
        """
        subprocess.call("rm " + os.path.join(BASE_DIR, "images", "tmp") + "/*", shell=True)

def deleteImage(path):
    if path == "":
        return
    subprocess.call("rm " + path, shell=True)

if __name__=="__main__":
    ImP = ImageProvider("cat")
    ImP.getImageBatch()
    ImP.cleanUp()
