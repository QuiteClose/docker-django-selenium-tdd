'''
Downloads the latest chromedriver binary for linux and places it in the
specified target directory.
'''

import json
import os
import sys
import urllib.request


def download_chrome_driver(target):
    API_ENDPOINT = 'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json'
    blob = urllib.request.urlopen(API_ENDPOINT).read()
    data = json.loads(blob.decode('utf-8'))
    driver_url = [record['url'] for record in data['channels']['Stable']['downloads']['chromedriver'] if 'linux' in record['platform']][0]
    urllib.request.urlretrieve(driver_url, '/tmp/chrome_driver.zip')
    os.system('unzip /tmp/chrome_driver.zip chromedriver-linux64/chromedriver -d /tmp')
    os.system('mv /tmp/chromedriver-linux64/chromedriver {}'.format(target))


if __name__ == '__main__':
    try:
        target = sys.argv[1]
    except IndexError:
        print('Usage: {} <target>'.format(sys.argv[0]))
    else:
        download_chrome_driver(target)
