import os
import sys
import time

import requests


def download(path):
    start = time.monotonic()
    file_name = str(path.split('/')[-1])
    try:
        r = requests.get(path, stream=True, timeout=5)
    except:
        return 0
    size = int(r.headers.get('Content-Length', 0))
    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    end = time.monotonic()
    duration = end - start
    sp = (((size * 8) / 1024) / 1024) / duration

    return sp


def upload(url):
    file_name = 'random7000x7000.jpg'
    if os.path.exists(file_name):
        size = os.path.getsize(file_name)
        with open(file_name, 'r+b') as f:
            files = {'file': (file_name, f.read())}

        start = time.monotonic()
        r = requests.post(url, files=files)
        end = time.monotonic()

        if r.status_code == 200:
            duration = end - start
            sp = (((size * 8) / 1024) / 1024) / duration
            return sp
        else:
            print("Requests status code is '{}'".format(r.status_code), file=sys.stderr)
            return -1
    else:
        print("No such file '{}'".format(file_name), file=sys.stderr)
        return -1


def test_f():
    speed_download = download('http://moscow.speedtest.rt.ru:8080/speedtest/random7000x7000.jpg')
    speed_upload = upload('http://moscow.speedtest.rt.ru:8080/speedtest/upload.php')
    return speed_download, speed_upload

