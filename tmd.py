import twint
import twint.output
from bs4 import BeautifulSoup
import requests
import re


def get_soup(html):
    if html is not None:
        soup = BeautifulSoup(html, 'lxml')
        return soup
    else:
        return


def get_media_tweets(target):
    """Get all the media tweets
    Returns a dict with a list of the photo urls and video urls

    Args:
        target (str): Twitter username

    Returns:
        dict: Dict with 'photo urls' and 'video urls' keys.
    """

    c = twint.Config()
    c.Username = target
    c.Store_object = True
    c.Hide_output = True
    c.Media = True
    twint.run.Search(c)
    tweets = twint.output.tweets_list

    photo_urls = []
    video_urls = []
    for item in tweets:
        url = f'https://twitter.com/{target}/status/{item.id}'
        if item.photos:
            photo_urls.append(url)
        if item.video:
            video_urls.append(url)

    tweets.clear()
    return {
        'photo urls': photo_urls,
        'video urls': video_urls
    }


headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/74.0.3729.169 Safari/537.36'
}


def get_photos_from_tweet(url):
    """ Get all the photo urls from a tweet

    Args:
        url (str): url to the tweet

    Returns:
        list: list with all photo urls
    """
    import requests
    burp0_url = "https://twitter.com:443/i/api/2/timeline/conversation/1366772495299317760.json?cards_platform=Web-12&include_cards=1&include_entities=true"
    burp0_cookies = {"personalization_id": "\"v1_eFieMYoGAFGOoQTEB5Ipag==\"", "guest_id": "v1%3A161771682848336730",
                     "gt": "1379430493989478404", "ct0": "c0657bc619006b1553d302ddc47b8ed7"}
    burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
                     "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate",
                     "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                     "x-guest-token": "1379430493989478404", "x-csrf-token": "c0657bc619006b1553d302ddc47b8ed7", "DNT": "1"}
    resp = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
    if resp.status_code == 200:
        json_resp = resp.json()




def download_profile():
    pass


def download_tweet():
    pass
