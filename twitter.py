# Copyright (C) 2019 Philip Woldhek
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import twint
import os
import requests
import youtube_dl
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from re import compile
from tqdm import tqdm


class Twitter:
    def __init__(self, output=False, get_photos=True, get_videos=True):
        self.output = output
        self.get_photos = get_photos
        self.get_videos = get_videos

    def get_tweets(self, target):
        c = twint.Config()
        c.Username = target
        c.Resume = "./resume/{0}_history_ids.txt".format(target)
        c.Store_object = True
        c.Hide_output = True
        c.Media = True
        if self.output is True:
            print("crawling {0}".format(target))
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

    @staticmethod
    def get_soup(html):
        if html is not None:
            soup = BeautifulSoup(html, 'lxml')
            return soup
        else:
            return

    def download_photos(self, target, urls):
        location = "./downloads/{0}".format(target)
        photo_location = "{0}/photos".format(location)
        if not os.path.exists(location):
            os.mkdir(location)
        if not os.path.exists(photo_location):
            os.mkdir(photo_location)
        if self.output is True and urls:
            iter_obj = tqdm(urls, desc="{0}: downloading photos".format(target), unit="photos")
        else:
            iter_obj = urls
        for tweet in iter_obj:
            headers = {
                'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
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
                if self.output is True:
                    print("Error requesting the webpage: {0}".format(result.status_code))

    def download_videos(self, target, urls):
        location = "./downloads/{0}".format(target)
        video_location = "{0}/videos".format(location)
        if not os.path.exists(location):
            os.mkdir(location)
        if not os.path.exists(video_location):
            os.mkdir(video_location)
        if self.output is True and urls:
            iter_obj = tqdm(urls, desc="{0}: downloading videos".format(target), unit="videos")
        else:
            iter_obj = urls
        for tweet in iter_obj:
            try:
                ydl_opts = {"outtmpl": "{0}/%(id)s.%(ext)s".format(video_location), "quiet": True}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([tweet,])
            except youtube_dl.utils.DownloadError as y:
                if self.output is True:
                    print(y)

    def main(self, usernames):
        if not os.path.exists("downloads"):
            os.mkdir("downloads")
        if not os.path.exists("resume"):
            os.mkdir("resume")
        for username in usernames:
            tweets = self.get_tweets(username)
            if self.get_photos is True:
                self.download_photos(tweets[0], tweets[1])
            if self.get_videos is True:
                self.download_videos(tweets[0], tweets[2])
