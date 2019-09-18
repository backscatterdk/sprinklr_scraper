"""Scrapes Sprinklr data"""


import logging
import argparse
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import instaloader
from instaloader import Post


def setup_logger(name, log_file, level=logging.INFO):
    """Function to setup multiple loggers"""

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def download_twitter_photo(tweet_url):
    """Downloads photos"""
    try:
        tweet_html = urlopen(tweet_url)
        soup = BeautifulSoup(tweet_html, 'lxml')
        img = soup.find(
            "div", {"class": "AdaptiveMedia-photoContainer js-adaptive-photo"})
        img_url = img.get('data-image-url')
        filename = tweet_url.split('.com/')[1].replace('/', '-') + '.jpg'
        urlretrieve(img_url, f'tweet_imgs/{filename}')
    except:
        TWITTER_LOGGER.exception(f'{tweet_url} was not downloaded')


def download_instagram_photo(instagram_url):
    try:
        shortcode = instagram_url.split('/')[-2]
        post = Post.from_shortcode(L.context, shortcode)
        L.download_post(post=post, target='instragram_posts')
    except:
        INSTAGRAM_LOGGER.exception(f'{instagram_url} was not downloaded')
        pass


# Set up argparse
PARSER = argparse.ArgumentParser(description='Scrape Sprinklr data.')
PARSER.add_argument('datafile', help='Path to your data file')
ARGS = PARSER.parse_args()

# Set up loggers
TWITTER_LOGGER = setup_logger('twitter_logger', 'twitter_logfile.log')
INSTAGRAM_LOGGER = setup_logger('instagram_logger', 'instagram_logfile.log')

# Read data
DATA = pd.read_csv(ARGS.datafile, low_memory=False)

# Twitter scrape
print('Scraping Twitter...')
TWITTER_DATA = DATA[DATA['SocialNetwork'] == 'TWITTER']['Permalink']
for tweet in tqdm(TWITTER_DATA):
    download_twitter_photo(tweet)

# Instagram scrape
L = instaloader.Instaloader()
print('Scraping Instagram...')
INSTAGRAM_DATA = DATA[DATA['SocialNetwork'] == 'INSTAGRAM']['Permalink']
for instagram_post in INSTAGRAM_DATA:
    download_instagram_photo(instagram_post)
