"""Scrapes Sprinklr photos from Facebook, Twitter, and Instagram
TODO: facebook scraper doesnt scrape the correct image
"""

import logging
import csv
import argparse
from pathlib import Path
from urllib.request import urlopen, urlretrieve
import pandas as pd
from bs4 import BeautifulSoup
import instaloader
from tqdm import tqdm


def scrape_facebook_photo(url, photo_folder):
    pass


def scrape_twitter_photo(tweet_url, tweet_photo_folder):
    """Scrapes photos from Twitter with bs4"""

    try:
        # Open post and make soup
        tweet_html = urlopen(tweet_url)
        soup = BeautifulSoup(tweet_html, 'lxml')

        # Find image using platform specific tag
        img = soup.find(
            "div", {"class": 'AdaptiveMedia-photoContainer js-adaptive-photo'})

        # Get image url using platform specific tag
        img_url = img.get('data-image-url')

        # Urls aren't allowed in filenames, so we change / to -
        filename = tweet_url.split('.com/')[1].replace('/', '-') + '.jpg'

        # Keep a log of changed filenames, for each social media
        with open(f'twitter_name_log.csv', 'w') as log_file:
            writer = csv.writer(log_file)
            writer.writerow([img_url, filename])

        # Scrape photo
        filepath = Path(tweet_photo_folder) / filename
        urlretrieve(img_url, filepath)

    except Exception as e:
        logging.exception(f'{tweet_url} was not scrapeed from Twitter')


def scrape_instagram_photo(instagram_post_url, instagram_photo_folder):
    """Scrapes photos from Instagram"""
    try:
        # Shortcode is the last part of instagram post url
        shortcode = instagram_post_url.split('/')[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.scrape_post(post=post, target=Path(instagram_photo_folder))
    except:
        logging.exception(
            f'{instagram_post_url} was not scrapeed from Instagram')


# Set up argparse
PARSER = argparse.ArgumentParser(description='Scrape IBN data.')
PARSER.add_argument('datafile', help='Path to your data file')
ARGS = PARSER.parse_args()

# Read data
DATA = pd.read_csv(ARGS.datafile, low_memory=False)

# Set up logging
logging.basicConfig(filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

# Initialize Instaloader
L = instaloader.Instaloader()

# Social medias and associated scraping functions
SO_ME_FUNCS = {'FACEBOOK': scrape_facebook_photo,
               'TWITTER': scrape_twitter_photo,
               'INSTAGRAM': scrape_instagram_photo}

for so_me, scrape_func in SO_ME_FUNCS.items():
    print(f'Scraping {so_me}...')

    # Get the post urls for each SoMe
    links = DATA[DATA['SocialNetwork'] == so_me]['Permalink']

    # Make a folder to put photos for each SoMe
    photo_folder = Path('photos') / f'{so_me}_imgs'
    Path.mkdir(photo_folder, parents=True, exist_ok=True)

    # Scrape photos
    for url in tqdm(links):
        scrape_func(url, photo_folder)
