#!/usr/bin/env python3

import requests
import os
import hashlib
import io

URL_BASE = "https://cse6040.gatech.edu/datasets/"

def on_vocareum():
    return os.path.exists('.voc')

def localize_file(filebase):
    if on_vocareum():
        local_dir = "../resource/asnlib/publicdata/"
    else:
        local_dir = ""
    return "{}{}".format(local_dir, filebase)

def download(filebase, local_dir="", url_base=URL_BASE, checksum=None):
    local_file = localize_file(filebase)
    if not os.path.exists(local_file):
        url = "{}{}".format(url_base, filebase)
        print("Downloading: {} ...".format(url))
        r = requests.get(url)
        with open(local_file, 'wb') as f:
            f.write(r.content)
            
    if checksum is not None:
        with io.open(local_file, 'rb') as f:
            body = f.read()
            body_checksum = hashlib.md5(body).hexdigest()
            assert body_checksum == checksum, \
                "Downloaded file '{}' has incorrect checksum: '{}' instead of '{}'".format(local_file,
                                                                                           body_checksum,
                                                                                           checksum)
    print("'{}' is ready!".format(local_file))
    return local_file

def download_dataset(filebases, **kwargs):
    for filebase, checksum in filebases.items():
        download(filebase, checksum=checksum, **kwargs)

# eof
