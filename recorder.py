import subprocess
import os
import time
import signal
from datetime import datetime
import dropbox
from dotenv import load_dotenv

load_dotenv()

DURATION = '300'
TOKEN = os.getenv("DROPBOX_TOKEN")
DROPBOX_PATH = os.getenv("DROPBOX_PATH")

def upload(resource, filename):
        dbx = dropbox.Dropbox(TOKEN)
        destinationfile = '%s/%s' % (DROPBOX_PATH, filename)
        print(destinationfile)
        with open(resource, 'rb') as f:
                dbx.files_upload(f.read(), destinationfile)
                print('uploaded')

def recordAudio(filename):
        proc_args = ['arecord', '-D' , 'plughw:1,0' , '-c' , '1',  '-r' , '44100' , '-f', 'S32_LE' , '-t' , 'wav' , '-V' , 'mono' , '-v' , '-d', DURATION ,filename]
        res = subprocess.call(proc_args)


def main():
        while True:
                filename =  '%s.wav' % datetime.today().isoformat()
                localfile = '/tmp/%s' % filename
                recordAudio(localfile)
                upload(localfile, filename)
                os.remove(filename)

main()