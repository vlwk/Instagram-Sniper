from constants import *
from functions import *
from user_list import USER_LIST

import csv
import datetime
import json
import time
import urllib.request
from urllib.request import Request

def getPhotoData(user, csv):
	json1 = getJson(gen(user, 1))["items"] # each photo (/media)
	json2 = getJson(gen(user, 2))["user"] # profile (/?__a=1)

	to_append = "" # temporary string which stores what is going to be added into the row before the row is written into the csv

	# for every post in json1, add it to csv1 (each user own csv)
	# and csv_combined (csv with all the photos from all the users combined)
	id1 = ""
	id2 = ""
	for idx in range(media_count_dict[user]):

		time.sleep(INTERVAL) # currently set to 0.5

		cnt1 = idx % 20; # index in json1 (20 items per page)
		cnt2 = idx % 12; # index in json2 (12 items per page)

		if (cnt1 == 0):
			json1 = getJson(gen(user, 1) + "?max_id=" + id1)["items"] # getting json from next page
		if (cnt2 == 0):
			json2 = getJson(gen(user, 2) + "&max_id=" + id2)["user"] # getting json from next page
		
		# some temporary variables to reduce time complexity
		tmp_json1 = json1[cnt1]
		tmp_json2 = json2["media"]["nodes"]

		row = ""

		for idx2 in range(len(HEADER_LIST1)):

			header = HEADER_LIST1[idx2]

			if (header == "created_time"):
				try:
					to_append = tmp_json1["caption"]["created_time"]
				except:
					to_append = tmp_json1["created_time"]
				to_append = str(convUnix(int(to_append)))
			if (header == "created_unix_time"):
				try:
					to_append = tmp_json1["caption"]["created_time"]
				except:
					to_append = tmp_json1["created_time"]

			if (header == "location"):
				try:
					to_append = tmp_json1["location"]['name']
				except:
					to_append = tmp_json1["location"]

			if (header == "id"):
				to_append = tmp_json1["id"]

			if (header == "caption"):
				try:
					to_append = tmp_json1["caption"]["text"]
				except:
					to_append = ""

			if (header == "code"):
				to_append = tmp_json1["code"]

			if (header == "comments"):
				to_append = tmp_json1["comments"]['count']

			if (header == "low_res"):
				to_append = tmp_json1["images"]["low_resolution"]["url"]
			if (header == "low_height"):
				to_append = tmp_json1["images"]["low_resolution"]["height"]
			if (header == "low_width"):
				to_append = tmp_json1["images"]["low_resolution"]["width"]

			if (header == "standard_res"):
				to_append = tmp_json1["images"]["standard_resolution"]["url"]
			if (header == "standard_height"):
				to_append = tmp_json1["images"]["standard_resolution"]["height"]
			if (header == "standard_width"):
				to_append = tmp_json1["images"]["standard_resolution"]["width"]

			if (header == "thumbnail_res"):
				to_append = tmp_json1["images"]["thumbnail"]["url"]
			if (header == "thumbnail_height"):
				to_append = tmp_json1["images"]["thumbnail"]["height"]
			if (header == "thumbnail_width"):
				to_append = tmp_json1["images"]["thumbnail"]["width"]

			if (header == "actual_res"):
				to_append = tmp_json2[cnt2]["display_src"]
			if (header == "actual_height"):
				to_append = tmp_json2[cnt2]["dimensions"]["height"]
			if (header == "actual_width"):
				to_append = tmp_json2[cnt2]["dimensions"]["width"]

			if (header == "likes"):
				to_append = tmp_json1["likes"]["count"]

			if (header == "link"):
				to_append = tmp_json1["link"]
			
			to_append = str(to_append)
			to_append = fix(to_append) # string processing

			if (idx2 == len(HEADER_LIST1) - 1):
				row += (to_append + "\n")
			else:
				row += (to_append + ",")

		# writing to csv
		csv.write(row)

		# get id for pagination (json1 stores 20 entries per page, json2 stores 12)
		if (cnt1 == 19):
			id1 = tmp_json1["id"]
		if (cnt2 == 11):
			id2 = json2["media"]["page_info"]["end_cursor"]

		if (idx % 5 == 4):
			print("user " + user + " done with " + str(idx + 1) + "/" + str(media_count_dict[user]) + " rows.")