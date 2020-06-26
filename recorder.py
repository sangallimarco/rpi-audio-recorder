from subprocess import Popen, PIPE
import os
import time
import signal
from datetime import datetime
import dropbox
from dotenv import load_dotenv

load_dotenv()

DURATION = '600'
TOKEN = os.getenv("DROPBOX_TOKEN")
DROPBOX_PATH = os.getenv("DROPBOX_PATH")
AUDIO_CARD = os.getenv("AUDIO_CARD")

def upload(resource, filename):
	dbx = dropbox.Dropbox(TOKEN)
	destinationfile = '%s/%s' % (DROPBOX_PATH, filename)
	print(destinationfile)
	with open(resource, 'rb') as f:
		dbx.files_upload(f.read(), destinationfile)
		print('uploaded')

def recordAudio(filename):
	arecord = Popen( ['arecord', '-f', 'S16_LE' ,'-c','1', '-r', '22050', '-t', 'raw', '-D', AUDIO_CARD, '-d', DURATION],  stdout=PIPE)
	lame = Popen(['lame' ,'-r', '-s', '22.05', '-m', 'm', '-b', '64' ,'-', filename],  stdin=arecord.stdout, stdout=PIPE)
	arecord.stdout.close()
	output = lame.communicate()[0] 

def main():
	while True:
		filename = '%s.mp3' % datetime.today().isoformat()
		localfile = '/tmp/%s' % filename
		recordAudio(localfile)
		upload(localfile, filename)
		os.remove(localfile)

main()