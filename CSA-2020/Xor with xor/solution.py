import re
import gzip
import zipfile
import speech_recognition as sr
from shutil import copyfileobj
from os import listdir, rename, mkdir


DATA_DIRECTORY = "data/"


def xor(data, key):
    return bytearray(((data[i] ^ key[i % len(key)]) for i in range(0, len(data))))


def xor_and_unzip():
    with open('xor-with-xor.bin', 'rb') as r:
        enc = r.read()
    dec = xor(enc, b'xor')
    with open('xor.zip', 'wb') as w:
        w.write(dec)

    mkdir(DATA_DIRECTORY)
    with zipfile.ZipFile('xor.zip', 'r') as z:
        z.extractall(DATA_DIRECTORY)


def combine(): 
    for name in listdir(DATA_DIRECTORY):
        new_name = re.sub(r'\D', '', name)
        rename(DATA_DIRECTORY + name, DATA_DIRECTORY + new_name)

    with open(r'flag.gz', 'wb') as w:
        for i in range(1000):
            with open(DATA_DIRECTORY + str(i), 'rb') as r:
                w.write(r.read())
    with gzip.open('flag.gz', 'r') as f_in, open('flag.wav', 'wb') as f_out:
        copyfileobj(f_in, f_out)


def flag():
    audio_file = 'flag.wav'
    r = sr.Recognizer()
    print("listening...")
    with sr.AudioFile(audio_file) as audio:
        audio_data = r.record(audio)
        text = r.recognize_google(audio_data)
    return text


if __name__ == '__main__':
    xor_and_unzip()
    combine()
    print(flag())
