# Used in main.py in createDownload()

from constants import *
from functions import *
from user_list import USER_LIST

import csv
import datetime
import json
import time
import urllib.request
from urllib.request import Request

def downloadPhotos(user):
	json2 = getJson(gen(user, 2))["user"] # profile (/?__a=1)
	id2 = ""
	num_photos = getMediaCount(user)
	print(user + " has " + str(num_photos) + " photos to download.")
	for idx in range(num_photos):
		time.sleep(INTERVAL)
		cnt2 = idx % 12
		if (cnt2 == 0):
			json2 = getJson(gen(user, 2) + "&max_id=" + id2)["user"] # getting json from next page
		tmp_json2 = json2["media"]["nodes"]
		downloadImage(tmp_json2[cnt2]["display_src"], genImageURL(user, num_photos - idx))
		if (cnt2 == 11):
			id2 = json2["media"]["page_info"]["end_cursor"]
		if (idx % 5 == 4):
			print("user " + user + " done with " + str(idx + 1) + "/" + str(num_photos) + " photos.")

def updatePhotos(user, year, month, day):
	json1 = getJson(gen(user, 1))["items"] # each photo (/media)
	json2 = getJson(gen(user, 2))["user"] # profile (/?__a=1)

	to_append = "" # temporary string which stores what is going to be added into the row before the row is written into the csv

	# for every post in json1, add it to csv1 (each user own csv)
	# and csv_combined (csv with all the photos from all the users combined)
	id1 = ""
	id2 = ""

	num_photos = getMediaCount(user)

	for idx in range(num_photos):

		time.sleep(INTERVAL) # currently set to 0.5

		cnt1 = idx % 20 # index in json1 (20 items per page)
		cnt2 = idx % 12 # index in json2 (12 items per page)

		if (cnt1 == 0):
			json1 = getJson(gen(user, 1) + "?max_id=" + id1)["items"] # getting json from next page
		if (cnt2 == 0):
			json2 = getJson(gen(user, 2) + "&max_id=" + id2)["user"] # getting json from next page
		
		# some temporary variables to reduce time complexity
		tmp_json1 = json1[cnt1]
		tmp_json2 = json2["media"]["nodes"]

		row = ""
		to_append = ""

		try:
			to_append = tmp_json1["caption"]["created_time"]
		except:
			to_append = tmp_json1["created_time"]

		to_append = convUnix(int(to_append))

		if (to_append < str(convNormal(year, month, day))):
			break

		downloadImage(tmp_json2[cnt2]["display_src"], genImageURL(user, num_photos - idx))
		print("ok")

		# get id for pagination (json1 stores 20 entries per page, json2 stores 12)
		if (cnt1 == 19):
			id1 = tmp_json1["id"]
		if (cnt2 == 11):
			id2 = json2["media"]["page_info"]["end_cursor"]