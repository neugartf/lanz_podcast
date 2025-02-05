import os, os.path, glob
from datetime import timedelta

import ffmpeg
import requests
from podgen import Podcast, Episode, Media
from tqdm import tqdm

URL = 'https://lanz-podcast.droplet.neugartf.com/'
EPISODES_TO_FETCH = 6

if __name__ == '__main__':
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/static/"
    print("running in " + os.path.dirname(os.path.abspath(__file__)))
    api_url = "https://mediathekviewweb.de/api/query"

    payload = '{"queries": [{"fields": ["title"], "query": "Markus Lanz vom"}, {"fields": ["channel"], "query": ' \
              '"zdf"}], "sortBy": "timestamp", "sortOrder": "desc", "future": "false", "offset": "0", ' \
              '"size": "' + str(EPISODES_TO_FETCH) + '"}'
    headers = {
        'Content-Type': 'text/plain'
    }

    response = requests.request("POST", api_url, headers=headers, data=payload).json()

    p = Podcast(
        name='Markus Lanz',
        description='Jeden Dienstag, Mittwoch und Donnerstag bietet der Moderator eine große Bandbreite an Gästen und '
                    'Vielfalt an Themen – politisch aktuell, gesellschaftspolitisch relevant, berührend, '
                    'unterhaltsam.',
        website='https://www.zdf.de/gesellschaft/markus-lanz',
        explicit=False,
        image=URL + 'cover.jpeg'
    )
    print("processing results")
    for result in tqdm(response['result']['results']):
        url_video_low = result['url_video_low']
        file_name = url_video_low.split('/')[-1]
        file_name = os.path.splitext(file_name)[0]
        if not os.path.isfile(os.path.join(THIS_FOLDER, file_name + '.mp3')):
            print("downloading " + url_video_low)
            path_to_downloaded_video = os.path.join(THIS_FOLDER, file_name + '.mp4')
            r = requests.get(url_video_low, allow_redirects=True, stream=True)
            with open(path_to_downloaded_video, 'wb') as fd:
                for chunk in r.iter_content(chunk_size=128):
                    fd.write(chunk)
            print("ffmpeg " + path_to_downloaded_video)
            ffmpeg.input(THIS_FOLDER + file_name + '.mp4').output(THIS_FOLDER + file_name + '.mp3', ac=1).overwrite_output().run()
        p.episodes += [
            Episode(
                title=result['title'],
                media=Media(URL + file_name + '.mp3', os.path.getsize(THIS_FOLDER + file_name + '.mp3'),
                            duration=timedelta(seconds=result['duration'])),
                summary=result['description'],
            )]
    print("writing rss feed")
    p.rss_file('static/podcast.xml', minimize=False)

    filelist = glob.glob(os.path.join(THIS_FOLDER, "*.mp4"))
    for f in filelist:
      os.remove(f)

