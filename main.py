# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os

import requests

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = "https://mediathekviewweb.de/api/query"

    payload = '{"queries": [{"fields": ["title"], "query": "Markus Lanz vom"}, {"fields": ["channel"], "query": ' \
              '"zdf"}], "sortBy": "timestamp", "sortOrder": "desc", "future": "false", "offset": "0", "size": "10"} '
    headers = {
        'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()

    for result in response['result']['results']:
        url_video_low = result['url_video_low']
        file_name = url_video_low.split('/')[-1]
        file = requests.get(url_video_low, allow_redirects=True)
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        my_file = os.path.join(THIS_FOLDER, file_name)
        open(my_file, 'wb').write(file.content)
