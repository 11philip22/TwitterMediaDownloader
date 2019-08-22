# MIT License
#
# Copyright (c) 2019 Philip
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


import os
import signal
import sys
from pickle import dump
from pickle import load
from queue import Queue
from re import compile
from threading import Thread
from time import sleep
from urllib.parse import urlparse

import requests
import twint
import youtube_dl
from bs4 import BeautifulSoup
from progressbar import ProgressBar

from utils import *


class Twitter(object):
    def __init__(self, usernames, location, get_videos=True,
                 ignore_errors=True, get_photos=True, output=True):
        self.get_photos = get_photos
        self.get_videos = get_videos
        self.queue = Queue()
        self.crawling = True
        self.usernames = usernames
        self.ignore_errors = ignore_errors
        self.location = location
        self.writer = Writer((0, 4))
        self.output = output

    @staticmethod
    def get_soup(html):
        if html is not None:
            soup = BeautifulSoup(html, 'lxml')
            return soup
        else:
            return

    def get_tweets(self, target):
        c = twint.Config()
        c.Username = target
        c.Resume = "./resume/{0}_history_ids.txt".format(target)
        c.Store_object = True
        c.Hide_output = True
        c.Media = True
        if self.output is True:
            write_to_screen(0, 0, "Twitter crawler:")
            write_to_screen(0, 1, "crawling {0}".format(target))
        twint.run.Search(c)
        tweets = twint.output.tweets_list

        photo_url = []
        video_url = []
        for item in tweets:
            url = "https://twitter.com/statuses/{0}".format(item.id)
            if item.photos:
                photo_url.append(url)
            if item.video:
                video_url.append(url)

        tweets.clear()

        return target, photo_url, video_url

    def download_photos(self, target, urls):
        if urls:
            location = "{0}twitter/{1}".format(self.location, target)
            photo_location = "{0}/photos".format(location)
            if not os.path.exists(location):
                os.mkdir(location)
            if not os.path.exists(photo_location):
                os.mkdir(photo_location)
            prefix_msg = "{0}: Downloading photos ".format(target)
            with ProgressBar(max_value=len(urls), fd=self.writer, prefix=prefix_msg) as pbar:
                current_len = 0
                headers = {
                    'User-Agent':
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/74.0.3729.169 Safari/537.36'}
                for tweet in urls:
                    result = requests.get(tweet, headers)
                    if result.status_code is 200:
                        content = result.content
                        soup = self.get_soup(content)
                        for link in soup.findAll('img', attrs={'src': compile("^https://pbs.twimg.com/media")}):
                            photo_url = link['src']
                            url_obj = urlparse(photo_url)
                            file_name = url_obj.path.replace("/media/", "")
                            path = "{0}/{1}".format(photo_location, file_name)
                            if not os.path.isfile(path):
                                with open(path, "wb") as file:
                                    file.write(requests.get(photo_url).content)
                    else:
                        print("Error requesting the webpage: {0}".format(result.status_code))
                        if self.ignore_errors is False:
                            exit(1)
                    if self.output is True:
                        current_len += 1
                        pbar.update(current_len)
                        write_to_screen(0, 3, "Twitter downloader:")

    def download_videos(self, target, urls):
        if urls:
            location = "{0}twitter/{1}".format(self.location, target)
            video_location = "{0}/videos".format(location)
            if not os.path.exists(location):
                os.mkdir(location)
            if not os.path.exists(video_location):
                os.mkdir(video_location)
            prefix_msg = "{0}: Downloading videos ".format(target)
            with ProgressBar(max_value=len(urls), fd=self.writer, prefix=prefix_msg) as pbar:
                current_len = 0
                for tweet in urls:
                    try:
                        ydl_opts = {"outtmpl": "{0}/%(id)s.%(ext)s".format(video_location), "quiet": True}
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([tweet, ])
                    except youtube_dl.utils.DownloadError as y:
                        print(y)
                        if self.ignore_errors is False:
                            exit(1)
                    if self.output is True:
                        current_len += 1
                        pbar.update(current_len)
                        write_to_screen(0, 3, "Twitter downloader:")
                    if len(urls) > 200:
                        sleep(0.5)

    def sigterm_handler(self, signal, frame):
        self.dump_queue()
        sys.exit(0)

    def dump_queue(self):
        with open("queue", "w") as file:
            dump(self.queue, file, protocol=4, fix_imports=False)

    def load_queue(self):
        with open("queue", "r") as file:
            self.queue = load(file, fix_imports=False, encoding="bytes")

    def downloader(self):
        if not os.path.exists("{0}twitter".format(self.location)):
            os.mkdir("{0}twitter".format(self.location))
        while not self.queue.empty() or self.crawling:
            tweets = self.queue.get()
            if self.get_photos is True:
                self.download_photos(tweets[0], tweets[1])
            if self.get_videos is True:
                self.download_videos(tweets[0], tweets[2])
        if self.output is True:
            write_to_screen(0, 4, "Done downloading!")

    def crawler(self):
        if not os.path.exists("resume"):
            os.mkdir("resume")
        for username in self.usernames:
            tweets = self.get_tweets(username)
            self.queue.put(tweets)
        self.crawling = False
        if self.output is True:
            write_to_screen(0, 1, "Done crawling!")

    def start(self):
        signal.signal(signal.SIGTERM, self.sigterm_handler)
        Thread(target=self.downloader).start()
        self.crawler()
