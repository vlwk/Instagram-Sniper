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
		cnt2 = idx % 12;
		if (cnt2 == 0):
			json2 = getJson(gen(user, 2) + "&max_id=" + id2)["user"] # getting json from next page
		tmp_json2 = json2["media"]["nodes"]
		downloadImage(tmp_json2[cnt2]["display_src"], genImageURL(user, num_photos - idx))
		if (cnt2 == 11):
			id2 = json2["media"]["page_info"]["end_cursor"]
		if (idx % 5 == 4):
			print("user " + user + " done with " + str(idx + 1) + "/" + str(getMediaCount(user)) + " photos.")
