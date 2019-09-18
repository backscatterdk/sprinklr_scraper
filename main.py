"""Scrapes IBM data"""
# TODO: facebook scraper doesnt download the correct image

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


def download_twitter_photo(tweet_url, photo_folder):
    """Downloads photos from Twitter"""
    try:
        tweet_html = urlopen(tweet_url)
        soup = BeautifulSoup(tweet_html, 'lxml')
        img = soup.find(
            "div", {"class": "AdaptiveMedia-photoContainer js-adaptive-photo"})
        img_url = img.get('data-image-url')
        filename = tweet_url.split('.com/')[1].replace('/', '-') + '.jpg'
        urlretrieve(img_url, photo_folder)
    except: facebook
        TWITTER_LOGGER.exception(f'{tweet_url} was not downloaded')


def download_instagram_photo(instagram_post_url, photo_folder):
    """Downloads photos from Instagram"""
    try:
        shortcode = instagram_post_url.split('/')[-2]
        post = Post.from_shortcode(L.context, shortcode)
        L.download_post(post=post, target='photo_folder')
    except:
        INSTAGRAM_LOGGER.exception(f'{instagram_post_url} was not downloaded')
        pass


def download_facebook_photo(facebook_post_url, photo_folder):
    """Downloads photos from Facebook"""
    facebook_html = urlopen(facebook_post_url)
    soup = BeautifulSoup(facebook_html, 'lxml')
    img = soup.find(
        "img", {"class": "scaledImageFitWidth img"})
    img_url = img.get('src')
    filename = facebook_post_url.split('.com/')[1].replace('/', '-') + '.jpg'
    urlretrieve(img_url, photo_folder)
    with open('facebook_name_log.csv', 'w') as log_file:
        facebook_writer = csv.writer(log_file)
        facebook_writer.writerow([img_url, filename])


# Set up argparse
PARSER = argparse.ArgumentParser(description='Scrape IBN data.')
PARSER.add_argument('datafile', help='Path to your data file')
ARGS = PARSER.parse_args()

# Set up loggers
TWITTER_LOGGER = setup_logger('twitter_logger', 'twitter_logfile.log')
INSTAGRAM_LOGGER = setup_logger('instagram_logger', 'instagram_logfile.log')

# Read data
DATA = pd.read_csv(ARGS.datafile, low_memory=False)

# Initialize Instaloader
L = instaloader.Instaloader()

# Scrape images from different SoMe
social_medias = ['FACEBOOK', 'TWITTER', 'INSTAGRAM']
for so_me in social_medias:
    print(f'Scraping {so_me}...')

    # Get the post urls for each SoMe
    links = DATA[DATA['SocialNetwork'] == so_me]['Permalink']

    # Make a folder to put photos for each SoMe
    photo_folder = f'photos/{so_me}_imgs')
    if not os.path.exists(photo_folder):
        os.mkdir(photo_folder)

    # Scrape photos
    for url in tqdm(links):
        if so_me == 'FACEBOOK':
            download_facebook_photo(url, photo_folder)
        if so_me == 'TWITTER':
            download_twitter_photo(url, photo_folder)
        if so_me == 'INSTAGRAM':
            download_instagram_photo(url, photo_folder)
