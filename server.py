#!/usr/bin/python3

from logging import getLogger
import os
import sys

from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)


ALL_IMAGES = []


def _getAllMemeFiles(work_dir: str = os.getcwd()):
    databse_path = os.path.join(work_dir, "database")
    all_files = [fileName for fileName in os.listdir(
        databse_path) if fileName.lower().endswith(".db")]
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


@ app.route("/")
def index():
    return render_template("index.html", allimages=ALL_IMAGES, length=str(len(ALL_IMAGES)))


@ app.route("/r")
@ app.route("/reload")
def reload():
    _loadAllMemes()
    return redirect(url_for('index'))


def startServer():

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

    app.run("0.0.0.0", port=3335, debug=debug)


if __name__ == "__main__":
    startServer()
