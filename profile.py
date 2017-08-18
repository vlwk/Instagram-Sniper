from constants import *
from functions import *
from user_list import USER_LIST

import csv
import datetime
import json
import time
import urllib.request
from urllib.request import Request

def getProfile(user, csv):
	json1 = getJson(gen(user, 1))["items"] # each photo (/media)
	json2 = getJson(gen(user, 2))["user"] # profile (/?__a=1)
	row = "" # start with empty row
	to_append = "" # temporary string which stores what is going to be added into the row before the row is written into the csv

	# add profile details of user from json2 into csv2
	for header in HEADER_LIST2:
		if (header != "profile_picture"):
			if (header == "followed_by" or header == "follows"):
				to_append = str(json2[header]["count"])
			elif (header == "media_count"):
				val = json2["media"]["count"]
				to_append = str(val)
			else:
				to_append = str(json2[header])
			to_append = fix(to_append)
			to_append += ","
			row += to_append
	prof_pic = json1[0]["caption"]["from"]["profile_picture"]
	to_append = str(prof_pic)
	to_append = fix(to_append)
	to_append += "\n"
	row += to_append
	csv.write(row)