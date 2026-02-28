import concurrent.futures
import os
import time

import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm import tqdm


class Podcast:
    """
    Downloads podcast episodes from an RSS feed concurrently.

    Class attributes:
        PODCAST_URL: RSS feed URL to scrape.
        PODCAST_NAME: Used as the download folder name.
        PODCASTS_TO_DOWNLOAD: Number of episodes to fetch from the feed.
    """

    PODCAST_URL = "https://runninginproduction.com/podcast/feed.xml"
    PODCAST_NAME = "Running in Production"
    PODCASTS_TO_DOWNLOAD = 5

    def __init__(self, url, name):
        """
        Args:
            url: RSS feed URL.
            name: Podcast name, used to create the download folder.
        """
        self.url = url
        self.folder = os.path.join(os.getcwd(), name)

    def setup_folder(self, folder=PODCAST_NAME):
        """Create the download folder if it doesn't already exist."""
        os.makedirs(self.folder, exist_ok=True)

    def get_episodes(self, limit=PODCASTS_TO_DOWNLOAD):
        """
        Fetch and parse episodes from the RSS feed.

        Args:
            limit: Maximum number of episodes to retrieve.

        Returns:
            A list of BeautifulSoup Tag objects, one per episode.
        """
        response = requests.get(self.url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "xml")
        return soup.find_all("item", limit=limit)

    def to_filename(self, string):
        """
        Sanitize a string into a valid filename by stripping illegal characters.

        Args:
            string: Raw episode title string.

        Returns:
            A filename-safe string with only alphanumerics and ' -_.#&' allowed.
        """
        return "".join(c for c in string if c.isalnum() or c in " -_.#&").strip()

    def download_episode(self, item):
        """
        Download a single episode and save it as an MP3.

        Intended to be called concurrently via ThreadPoolExecutor.

        Args:
            item: A BeautifulSoup Tag object representing an RSS <item>.

        Returns:
            A summary string with the filename and size, e.g. '#001 - Title (45.2 MB)'.
        """

        @retry(
            stop=stop_after_attempt(5),
            wait=wait_exponential(multiplier=1, min=2, max=32),
        )
        def _download():
            with requests.get(mp3_url, stream=True, timeout=30) as r:
                r.raise_for_status()
                with open(file_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

        title = item.find("title").text
        episode = int(item.find("link").text.split("/")[-1].split("-")[0])
        mp3_url = item.find("enclosure")["url"]
        mp3_size_mb = round(int(item.find("enclosure")["length"]) / (1024**2), 2)
        file_name = self.to_filename(f"#{episode:03d} - {title}")
        file_path = os.path.join(self.folder, f"{file_name}.mp3")

        _download()

        return f"{file_name} ({mp3_size_mb} MB)"


if __name__ == "__main__":
    start = time.perf_counter()

    podcast = Podcast(url=Podcast.PODCAST_URL, name=Podcast.PODCAST_NAME)
    podcast.setup_folder()

    print("Fetching episode list...")
    episodes = podcast.get_episodes()
    print(f"Found {len(episodes)} episodes. Starting download...\n")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(podcast.download_episode, ep): ep for ep in episodes}
        with tqdm(total=len(futures), unit="episode") as progress:
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    progress.set_postfix_str(result)
                    progress.update(1)
                except Exception as e:
                    progress.write(f"Download failed: {e}")
                    progress.update(1)

    elapsed = round(time.perf_counter() - start, 2)
    print(f"\nFinished {len(episodes)} episodes in {elapsed}s")
