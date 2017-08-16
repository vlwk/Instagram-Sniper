# Written in Python 3.6.2 by Victor Loh

import csv
import datetime
import json
import time
import urllib.request
from urllib.request import Request

interval = 0.5

# for extraction of each photo
header_list1 = ["created_unix_time", "created_time", "location", "id", "caption", "code", "comments", "low_res", "low_height", "low_width", "standard_res", "standard_height", "standard_width", "thumbnail_res", "thumbnail_height", "thumbnail_width", "actual_res", "actual_height", "actual_width", "likes", "link"]

# for collection of profile details (mostly for fun)
header_list2 = ["username", "full_name", "id", "biography", "external_url", "external_url_linkshimmed", "followed_by", "follows", "is_private", "is_verified", "media_count", "profile_picture"]

# dictionary to store number of posts per user
media_count_dict = {}

# user_agent used to make requests
user_agent = 'Mozilla/5.0 (Macintosh; Intel MAC OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'

# list of users
user_list = ["99.co", "sgig", "visit_singapore", "dparchitects", "wow_architects", "k2ld.architects.sg", "thescientistpteltd"]

# print an indented version of a json file
def beautify(file):
	return json.dumps(file, sort_keys=True, indent=2)

# convert from unixtime to a standard time format
def convUnix(unixTime):
	import datetime
	return datetime.datetime.fromtimestamp(unixTime).strftime('%Y-%m-%d %H:%M:%S')

# generate url (1 for each photo, 2 for profile details)
def gen(user, sel):
	url = "https://www.instagram.com/"
	if (sel == 1):
		return url + user + "/media/"
	if (sel == 2):
		return url + user + "/?__a=1"

# get json file from a url, can use together with beautify
def getJson(url):
	request = Request(url, headers = {'User-agent': user_agent})
	request.add_header('api-key', '200')
	return json.loads(urllib.request.urlopen(request).read().decode('utf8'))

# generate row of comma separated headers for csv for each photo
def header1(csv1):
	headerRow = ""
	for header in header_list1:
		if (header == "link"):
			headerRow += (header + "\n")
		else:
			headerRow += (header + ",")
	csv1.write(headerRow)

# generate row of comma separated headers for csv of profile details
def header2():
	headerRow = ""
	for header in header_list2:
		if (header == "profile_picture"):
			headerRow += (header + "\n")
		else:
			headerRow += (header + ",")
	csv2.write(headerRow)

# string processing to make sure there are no unwanted commas or newlines in each row
def fix(to_append):
	to_append = to_append.replace('\n', ' ')
	to_append = to_append.replace(',', ' ')
	to_append = to_append.lstrip(' ')
	return to_append

def run(user):
	json1 = getJson(gen(user, 1))["items"] # each photo (/media)
	json2 = getJson(gen(user, 2))["user"] # profile (/?__a=1)
	row = "" # start with empty row
	to_append = "" # temporary string which stores what is going to be added into the row before the row is written into the csv

	# add profile details of user from json2 into csv2
	for header in header_list2:
		if (header != "profile_picture"):
			if (header == "followed_by" or header == "follows"):
				to_append = str(json2[header]["count"])
			elif (header == "media_count"):
				val = json2["media"]["count"]
				to_append = str(val)
				media_count_dict[user] = int(val)
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
	csv2.write(row)
	print("USER: " + user + " DONE WITH PROFILES (" + str(cnt) + "/" + str(len(user_list)) + ")")

	# for every post in json1, add it to csv1 (each user own csv)
	# and csv_combined (csv with all the photos from all the users combined)
	id1 = ""
	id2 = ""
	for idx in range(media_count_dict[user]):
		time.sleep(interval) # currently set to 0.5

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
		for header in header_list1:
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

			# a bit spammy
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
			if (header == "likes"):
				to_append = tmp_json1["likes"]["count"]
			if (header == "link"):
				to_append = tmp_json1["link"]

			# although we get profile details from json2, it contains some information on each photo as well which we extract
			if (header == "actual_res"):
				to_append = tmp_json2[cnt2]["display_src"]
			if (header == "actual_height"):
				to_append = tmp_json2[cnt2]["dimensions"]["height"]
			if (header == "actual_width"):
				to_append = tmp_json2[cnt2]["dimensions"]["width"]
			
			to_append = str(to_append)
			to_append = fix(to_append) # string processing

			if (header == "link"):
				row += (to_append + "\n")
			else:
				row += (to_append + ",")

		# writing to csv
		csv1.write(row)
		csv_combined.write(row)

		# get id for pagination (json1 stores 20 entries per page, json2 stores 12)
		if (cnt1 == 19):
			id1 = tmp_json1["id"]
		if (cnt2 == 11):
			id2 = json2["media"]["page_info"]["end_cursor"]

		if (idx % 5 == 4):
			print("user " + user + " done with " + str(idx + 1) + "/" + str(media_count_dict[user]) + " rows, cnt1: " + str(cnt1) + ", cnt2: " + str(cnt2))

# combining everything together
csv2 = open("profiles.csv", "w")
csv_combined = open("combined.csv", "w")

header1(csv_combined) # write header1 row to csv_combined (all the csv1 in a single csv)
header2() # write header2 row to csv2 (all the user profiles)

to_process = {}

num_users = 0
for user in user_list:
	ask = int(input("Would you like to process " + user + "? 1 for YES, 0 for NO: "))
	to_process[user] = ask
	if (ask == 1):
		num_users += 1

cnt = 0
for user in user_list:
	csv1 = open(user + ".csv", "w")
	header1(csv1) # write header1 row to csv1 (each user)
	if (to_process[user] == 1):
		run(user)
		cnt += 1
		print("USER: " + user + " DONE WITH EXTRACTION (" + str(cnt) + "/" + str(num_users) + ")")
	csv1.close()

csv2.close()
csv_combined.close()

# print(beautify(getJson(gen("99.co", 2))))