# jack Muskopf
# jam.muskopf at gmail dot com


import sys
import os
import shutil
import eyed3
import time

def clean_name(string):
	return string.strip().replace('\\','-').replace('/','-').encode('ascii','ignore')


def confirm_dirs(artist,album):
	
	art_dir = os.path.join(OUT_FOLDER,artist)
	if not os.path.isdir(art_dir):
		os.mkdir(art_dir)

	alb_dir = os.path.join(art_dir,album)
	if not os.path.isdir(alb_dir):
		os.mkdir(alb_dir)

	return alb_dir

def try_get_artist(af):
	try:
		tag = af.tag
		artist = clean_name(tag.artist)
		artist = artist if artist else 'Unknown Artist'
	except Exception as e:
		# print(e)
		artist = 'Unknown Artist'
	return artist

def try_get_album(af):
	try:
		tag = af.tag
		album = clean_name(tag.album)
		album = album if album else 'Unknown Album'
	except Exception as e:
		# print(e)
		album = 'Unknown Album'
	return album

def try_get_title(af):
	try:
		tag = af.tag
		title = clean_name(tag.title)
		title = title if title else 'Untitled'
	except Exception as e:
		# print(e)
		title = 'Untitled'
	return title


MUSIC_FOLDER = "/Volumes/500GB SSD/mickeys_ipod/iPod_Control/Music"

OUT_FOLDER = "/Volumes/500GB SSD/recovered_music2"

items = [os.path.join(dp, f) for dp, dn, filenames in os.walk(MUSIC_FOLDER) for f in filenames]

files = [i for i in items if os.path.isfile(i)]


print('Found {} files.'.format(len(files)))

time.sleep(2)



dups = []


failed = []
for n,fname in enumerate(files):
	try:
		af = eyed3.load(fname)
		artist = try_get_artist(af)
		album = try_get_album(af)
		song = try_get_title(af)
	except Exception as e:
		artist = try_get_artist(None)
		album = try_get_album(None)
		song = try_get_title(None)
		# print(e)



	if n%100 == 0:
		print("percent done: {}%".format(100*n/float(len(files))))

	song_dir = confirm_dirs(artist,album)

	song_ext = os.path.split(fname)[-1].split('.')[-1]
	song_ext = song_ext if song_ext in ['wav', 'mov', 'm4a', 'mp3', 'm4p'] else ''
	song_path = os.path.join(song_dir,"{}.{}".format(song,song_ext))
	# print(song_path)
	
	already_exists = os.path.isfile(song_path)
	if already_exists:
		dups.append(song_path)
		ix = 1
		while already_exists:
			song_path = os.path.join(song_dir,"{}_{}.{}".format(song,ix,song_ext))
			already_exists = os.path.isfile(song_path)
			ix += 1

	shutil.copyfile(fname,song_path)

