from constants import *
from user_list import USER_LIST

import csv
import datetime
import json
import time
import urllib.request
from urllib.request import Request

# print an indented version of a json file
def beautify(file):
	return json.dumps(file, sort_keys=True, indent=2)

# convert from unixtime to a standard time format
def convUnix(unixTime):
	import datetime
	return datetime.datetime.fromtimestamp(unixTime).strftime('%Y-%m-%d %H:%M:%S')

def downloadImage(url, fileName):
	urllib.request.urlretrieve(url, fileName)

# generate url (1 for each photo, 2 for profile details)
def gen(user, sel):
	if (sel == 1):
		return BASE_URL + user + "/media/"
	if (sel == 2):
		return BASE_URL + user + "/?__a=1"

def genImageURL(user, idx):
	return user + "/" + user + str(idx) + ".jpg"

# get json file from a url, can use together with beautify
def getJson(url):
	request = Request(url, headers = {'User-agent': USER_AGENT})
	request.add_header('api-key', '200')
	return json.loads(urllib.request.urlopen(request).read().decode('utf8'))

# generate row of comma separated headers for csv for each photo
def genHeader(header_list):
	headerRow = ""
	for idx in range(len(header_list)):
		header = header_list[idx]
		if (idx == len(header_list) - 1):
			headerRow += (header + "\n")
		else:
			headerRow += (header + ",")
	return headerRow

# string processing to make sure there are no unwanted commas or newlines in each row
def fix(to_append):
	to_append = to_append.replace('\n', ' ')
	to_append = to_append.replace(',', ' ')
	to_append = to_append.lstrip(' ')
	return to_append

def getMediaCount(user):
	json2 = getJson(gen(user, 2))["user"]
	return int(json2["media"]["count"])
