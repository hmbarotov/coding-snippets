import concurrent.futures
import os
import time

import requests
from bs4 import BeautifulSoup

# Timing the script
f1 = time.perf_counter()

WORK_DIR = os.getcwd()
PODCAST_URL = "https://runninginproduction.com/podcast/feed.xml"  # Podcast RSS
PODCAST_NAME = "Running in Production"  # Podcast name for folder naming
PODCASTS_TO_DOWNLOAD = 1  # Number of podcasts to download


class Podcast:
    """
    Main class to download podcasts
    """

    def __init__(self, url):
        self.url = url

    def create_folder(self, folder=PODCAST_NAME):
        """
        Create a 'downloads' folder.
        """
        os.makedirs(folder, exist_ok=True)
        return os.path.join(WORK_DIR, folder)

    def get_podcasts(self, limit=PODCASTS_TO_DOWNLOAD):
        """
        Scrape the RSS feed and get podcasts
        """
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "xml")
        podcasts = soup.find_all("item", limit=limit)
        return podcasts

    def get_size(self, length):
        """
        Get the size of a podcast, in MB
        """
        return round(length / (1024**2), 2)

    def convert_to_valid_name(self, string):
        """
        Convert podcast names to valid filenames
        """
        filename = (
            "".join(c for c in string if c.isalnum() or c in " -_.#&").strip() + ".mp3"
        )
        return os.path.splitext(filename)[0]

    def download_podcast(self, podcast):
        """
        Download podcasts using threading
        """

        title = podcast.find("itunes:title").text or podcast.find("title").text
        episode = int(podcast.find("itunes:episode").text)

        mp3_url = podcast.find("enclosure")["url"] or podcast.find("link").text
        mp3_size = self.get_size(int(podcast.find("enclosure")["length"]))
        file_name = self.convert_to_valid_name(f"#{episode:03d} - {title}")
        folder = self.create_folder()

        print(f">>> Downloading {file_name} ({mp3_size} MB)")

        with requests.get(mp3_url, stream=True) as r:
            r.raise_for_status()  # Ensure the download actually starts
            with open(os.path.join(folder, f"{file_name}.mp3"), "wb") as f:
                for data in r.iter_content(chunk_size=8192):
                    f.write(data)

        print(f">>> Finished: {file_name}")


if __name__ == "__main__":
    print("Starting podcast downloader...")
    podcast = Podcast(url=PODCAST_URL)

    # Choose podcasts here by slicing
    # Choosing the first N podcasts
    print("Fetching podcast list...")
    podcasts = podcast.get_podcasts(limit=PODCASTS_TO_DOWNLOAD)

    print(f"Found {len(podcasts)} podcasts to download.")
    # Using threading to speed up downloads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(podcast.download_podcast, podcasts)

f2 = time.perf_counter()

print(f"Script finished in {round(f2 - f1, 2)} second(s)")
