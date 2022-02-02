#!/usr/bin/python3

import json
import os
import sys
from logging import getLogger
import random

from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)


ALL_IMAGES = []

# load settings
with open(str(os.path.join(os.getcwd(), "database", "config.json")), "r", encoding="utf-8") as fdata:
    settings = json.load(fdata)


def _getAllMemeFiles(work_dir: str = os.getcwd()):
    databse_path = os.path.join(work_dir, "database")
    all_files = [fileName for fileName in os.listdir(
        databse_path) if fileName.lower().endswith(settings["LinkFilesEnding"])]
    return all_files


def _loadAllMemes():
    global ALL_IMAGES

    for fileName in _getAllMemeFiles(work_dir=str(os.getcwd())):
        try:
            with open(os.path.join(str(os.getcwd()), "database", str(fileName)), "r", encoding="utf-8") as temp1:
                all_lines = temp1.read().splitlines()
                for line in all_lines:
                    if not(line in ALL_IMAGES):
                        ALL_IMAGES.append(str(line).strip())
        except:
            pass


@app.route("/")
def index():
    global settings

    if len(ALL_IMAGES) == 0:
        _loadAllMemes()

    instagram_links = []
    facebook_links = []
    twitter_links = []
    for key1, value1 in settings["Website"]["Social1"].items():
        if key1 == "Facebook":
            if isinstance(value1, list):
                for valuesfb in value1:
                    facebook_links.append(valuesfb)
            else:
                facebook_links.append(value1)
        if key1 == "Instagram":
            if isinstance(value1, list):
                for valuesig in value1:
                    instagram_links.append(valuesig)
            else:
                instagram_links.append(value1)
        if key1 == "Twitter":
            if isinstance(value1, list):
                for valuetw in value1:
                    twitter_links.append(valuetw)
            else:
                twitter_links.append(value1)

    return render_template("index.html",
                           allimages=ALL_IMAGES,
                           length=str(len(ALL_IMAGES)),
                           wblocation=settings["Website"]["Location"],
                           wbcontact=settings["Website"]["Contact"],
                           wbemail=settings["Website"]["Email"],
                           wbcopyright=settings["Website"]["Copyright"],
                           instagram_links=instagram_links,
                           facebook_links=facebook_links,
                           twitter_links=twitter_links,
                           bottom_links=settings["Website"]["Bottom"],
                           SecretKey=settings["SecretKey"]
                           )


@app.route("/r")
@app.route("/reload")
def reload():
    _loadAllMemes()
    return redirect(url_for('index'))


@app.route("/api")
def api():
    if len(ALL_IMAGES) == 0:
        _loadAllMemes()
    return {"image": random.choice(ALL_IMAGES)}


def startServer():

    global settings

    def _disable_werkzeug():
        app.logger.disabled = True
        ueslessLogger = getLogger('werkzeug')
        ueslessLogger.disabled = True

    debug = True
    try:
        if str(sys.argv[1]).lower().startswith("d"):
            debug = True
        else:
            debug = False
            _disable_werkzeug()
    except:
        _disable_werkzeug()

    app.run(settings["HOST"], port=int(settings["PORT"]), debug=debug)


if __name__ == "__main__":
    startServer()
