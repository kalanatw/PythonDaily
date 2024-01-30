
from pytube import YouTube
from pytube import Playlist
from pytube.exceptions import VideoUnavailable
from http.client import IncompleteRead
import requests

SAVE_PATH = ""  # to_do

# link of the video or playlist to be downloaded
links = ""

playlist = Playlist(links)

PlayListLinks = playlist.video_urls
N = len(PlayListLinks)

print(f"This link found to be a Playlist Link with the number of videos equal to {N} ")
print(f"\n Let's Download all {N} videos")

for i, link in enumerate(PlayListLinks):
    try:
        yt = YouTube(link)
    except VideoUnavailable:
        print(f'Video {link} is unavailable, skipping.')
        continue

    retries = 3
    while retries > 0:
        try:
            d_video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            d_video.download(SAVE_PATH)
            print(f"{i+1} Video is Downloaded.")
            break  # Successful download, exit the loop
        except IncompleteRead:
            print(f"IncompleteRead error. Retrying... ({retries} retries left)")
            retries -= 1
        except requests.exceptions.RequestException as e:
            print(f"RequestException error. Retrying... ({retries} retries left)")
            retries -= 1
    else:
        print(f"Failed to download {link}. Skipping.")

print("Download completed.")

