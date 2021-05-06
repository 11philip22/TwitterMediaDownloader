import unittest

from tmd import *


class TestTmd(unittest.TestCase):
    def test_get_tweets(self):
        target_username = 'philipwoldhek'
        tweets = get_media_tweets(target_username)
        self.assertTrue(tweets)

    def test_photos_from_tweet(self):
        test_tweet = 'https://twitter.com/philipwoldhek/status/1366772495299317760'
        get_photos_from_tweet(test_tweet)


if __name__ == '__main__':
    unittest.main()
