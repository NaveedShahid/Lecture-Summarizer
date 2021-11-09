from __future__ import division

import os
import io
import re
import sys
import shlex
import subprocess
import time
import argparse
import pyaudio
import numpy as np

from six.moves import queue
from io import BytesIO
from google.cloud import storage
from google.cloud import speech
from bart_summarizer import do_summarize

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

path_to_json = "dazzling-ego-297009-6e03c87d770b.json"

def process_mp3(path):
    if not os.path.isdir(path):
        if str(path.split('.')[1])=='mp3':
            path1 = path
            path2 = str(path.split('.')[0]) + ".flac"
            path3 = str(path.split('.')[0]) + "_processed.flac"

            convert_mp3 = "ffmpeg -i "+path1+" "+path2
            ffmpeg_pid = subprocess.call(shlex.split(convert_mp3))
            
            ffmpeg_code = "ffmpeg -i "+path2+" -ar 16000 -ac 1 "+path3
            ffmpeg_pid2 = subprocess.call(shlex.split(ffmpeg_code))
            os.remove(path2)
            return path3
    else:
        print("Please pass path to the mp3 file")
        sys.exit()

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""

    storage_client = storage.Client.from_service_account_json(path_to_json)

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

    os.remove(source_file_name)
    return blob.public_url

def transcribe_audio(path):
    from google.cloud import speech
    
    flac_file=process_mp3(path)
    uri_=upload_blob("audio_1_new",flac_file, flac_file.split('/')[-1])
    uri = "gs:/"+uri_.split('.com')[-1]
    client = speech.SpeechClient.from_service_account_json(path_to_json)

    audio = speech.RecognitionAudio(uri=uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code="en-US",
        model="video",
        enable_automatic_punctuation=True,
    )

    operation = client.long_running_recognize(
        request={"config": config, "audio": audio}
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=2000)
    
    lines=[]
    with open("transcript.txt", "a") as f:
        for result in response.results:
            line=result.alternatives[0].transcript
            f.write(line)
            lines.append(line)
        f.close()
    text='.'.join(map(str, lines))
    return text
