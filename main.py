import os
from datetime import timedelta

import ffmpeg
from podgen import Podcast, Episode, Media

import requests

URL = 'http://lanz.neugartf.com:8080/'
EPISODES_TO_FETCH = 6

if __name__ == '__main__':
    api_url = "https://mediathekviewweb.de/api/query"

    payload = '{"queries": [{"fields": ["title"], "query": "Markus Lanz"},{"fields": ["description"], "query": "Zu ' \
              'Gast:"}, {"fields": ["channel"], "query": ' \
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
        image='https://www.zdf.de/assets/logo-markus-lanz-102~314x314?cb=1539075488568'
    )

    for result in response['result']['results']:
        url_video_low = result['url_video_low']
        file_name = url_video_low.split('/')[-1]
        file_name = os.path.splitext(file_name)[0]
        file = requests.get(url_video_low, allow_redirects=True)
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        my_file = os.path.join(THIS_FOLDER, file_name + '.mp4')
        open(my_file, 'wb').write(file.content)
        ffmpeg.input(file_name + '.mp4').output(file_name + '.mp3', ac=1).overwrite_output().run()
        p.episodes += [
            Episode(
                title=result['description'],
                media=Media(URL + file_name + '.mp3', os.path.getsize(file_name + '.mp3'),
                            duration=timedelta(seconds=result['duration'])),
                summary=result['description'],
            )]

    p.rss_file('podcast.xml', minimize=False)
