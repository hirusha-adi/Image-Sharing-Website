#!/usr/bin/python3

import logging
import os
from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for
from user_agents import parse


# Config for logs
if 'logs' not in os.listdir(os.getcwd()):
    os.mkdir("logs")

cur_time = datetime.now()
log_file_name = f'logs/LOG {cur_time.day}.{cur_time.month}.{cur_time.year} - {cur_time.hour}-{cur_time.minute}-{cur_time.second}.log'
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    filename=log_file_name,
                    filemode='w',
                    level=logging.INFO)

# Flask App
app = Flask(__name__)
logging.debug("Created Flask app")
app.logger.disabled = True
ueslessLogger = logging.getLogger('werkzeug')
ueslessLogger.disabled = True

# Store all image links
ALL_MEMES = []


def _getAllMemeFiles(work_dir: str = os.getcwd()):
    """
    Get the text files list in the directory

    Args:
        work_dir (str, optional): Working Directory with the 'database' folder in it. Defaults to 'os.getcwd()'.

    Returns:
        list (Iterable): All text files in work_dir/database
    """
    logging.debug("Running '_getAllMemeFiles()'")

    databse_path = os.path.join(work_dir, "database")
    all_files = [fileName for fileName in os.listdir(
        databse_path) if fileName.lower().endswith(".txt")]

    logging.info(f"Found {len(all_files)} '.txt' files  in './database/'")
    logging.debug("Returning list from '_getAllMemeFiles()'")

    return all_files


def _loadAllMemes():
    """
    Load media links pasted in the text files (seperated by lines)
    and add it to the 'ALL_MEMES' global variable
    """

    global ALL_MEMES

    logging.debug("Running '_loadAllMemes()'")

    for fileName in _getAllMemeFiles(work_dir=str(os.getcwd())):
        try:
            logging.debug(f"Opening ./database/{fileName}")
            with open(os.path.join(str(os.getcwd()), "database", str(fileName)), "r", encoding="utf-8") as temp1:
                all_lines = temp1.read().splitlines()
                logging.debug(
                    f"Stripped all lines successfully in ./database/{fileName}")

                for line in all_lines:
                    if not(line in ALL_MEMES):
                        ALL_MEMES.append(str(line).strip())
                        logging.debug("Added image link to 'ALL_MEMES'")

        except FileNotFoundError:
            logging.error(
                f"File Not Found: {os.path.join(str(os.getcwd()), 'database', str(fileName))}. Raisd from '_loadAllMemes()'")

        except Exception as e:
            logging.error(f"Error: {e}. Raised from '_loadAllMemes()'")


@app.route("/")
def index():
    # Collecting User Data Manually for security purposes
    try:
        ua = parse(request.headers.get("User-Agent"))
    except:
        ua = "Unable to parse UA"
    try:
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    except:
        ip = "Unable to get IP"

    logging.info(
        f"{ip} requested to reload the meme database -->\n\tBrowser Family: {ua.browser.family}\n\tBrowser Version: {ua.browser.version_string}\n\tOS Family: {ua.os.family}\n\tDevice Model: {ua.device.model}\n\tDevice Brand: {ua.device.brand}")

    return render_template("index.html", allmemes=ALL_MEMES, length=str(len(ALL_MEMES)))


@app.route("/r")
@app.route("/re")
@app.route("/reload")
def reload():
    # Collecting User Data Manually for security purposes
    try:
        ua = parse(request.headers.get("User-Agent"))
    except:
        ua = "Unable to parse UA"
    try:
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    except:
        ip = "Unable to get IP"
    logging.info(
        f"{ip} requested to reload the meme database -->\n\tBrowser Family: {ua.browser.family}\n\tBrowser Version: {ua.browser.version_string}\n\tOS Family: {ua.os.family}\n\tDevice Model: {ua.device.model}\n\tDevice Brand: {ua.device.brand}")

    _loadAllMemes()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run("0.0.0.0", port=3335, debug=False)
