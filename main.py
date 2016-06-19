import os
import sys
import random
import urllib.request
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, json

ic = Flask(__name__)


@ic.route("/")
def main():
    return render_template("index.html")


@ic.route("/get_images", methods=['POST'])
def get_images():
    _url = request.form['inputURL']
    try:
        count = 0
        code = requests.get(_url)
        text = code.text
        soup = BeautifulSoup(text)
        for img in soup.findAll('img'):
            count += 1
            if (img.get('src'))[0:4] == 'http':
                src = img.get('src')
            else:
                src = urljoin(_url, img.get('src'))
            download_image(src, count)
        if count == 1:
            return render_template("index.html", result=str((str(count) + " Image Downloaded !")))
        else:
            return render_template("index.html", result=str((str(count) + " Images Downloaded !")))
    except requests.exceptions.HTTPError as error:
        return render_template("index.html", result=str(error))


def download_image(url, count):
    try:
        image_name = str(count) + ".jpg"
        image_path = os.path.join("images/", image_name)
        urllib.request.urlretrieve(url, image_path)
    except ValueError:
        print("Invalid URL !")
    except:
        print("Unknown Exception" + str(sys.exc_info()[0]))


if __name__ == "__main__":
    ic.run()
