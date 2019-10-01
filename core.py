# MIT License
#
# Copyright (c) 2019 Philip Woldhek
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
This script is a proof of concept.
I highly encourage you to incorporate the Twitter class in your own program.
"""

from sys import argv
import logging
from pathlib import Path
from os import getcwd

import urltools
from twitter import Twitter

log_name = "twitter_media_downloader"

fs_location = getcwd()
log_folder_path = Path(fs_location, "logs")
if not log_folder_path.is_dir():
    log_folder_path.mkdir()

file_name_increment = 0
while Path(log_folder_path, "{0}{1}.log".format(log_name, file_name_increment)).is_file():
    file_name_increment += 1

log_file_path = Path(log_folder_path, "{0}{1}.log".format(log_name, file_name_increment))
if not log_file_path.is_file():
    log_file_path.touch()

logger = logging.getLogger(log_name)
logger.setLevel(logging.INFO)
fh = logging.FileHandler(str(log_file_path))
fh.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


def get_list():
    print("Enter/Paste your usernames")
    contents = []
    while True:
        line = input()
        if line:
            contents.append(line)
        else:
            break
    if contents:
        return contents
    else:
        print("Enter/Paste urls")
        exit(1)


def get_content():
    if len(argv) < 2:
        content = get_list()
        return content
    else:
        file = argv[1]
        try:
            content = []
            list1 = list(open(file, "r"))
            links = list1[:] = [line.rstrip('\n') for line in list1]
            for item in links:
                if item:
                    url_info = urltools.extract(item)
                    if url_info[4] == str("twitter"):
                        item = url_info[7].replace("/", "")
                        content.append(item)
            return content
        except FileNotFoundError:
            print("File {0} not found!".format(argv[1]))
            exit(1)


if __name__ == "__main__":
    usernames = get_content()
    location = "./"
    t = Twitter(usernames=usernames, location=location, logger="{0.module}".format(log_name))
    t.start()
