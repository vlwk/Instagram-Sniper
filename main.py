# Refer to README

from constants import *
from functions import *
from user_list import USER_LIST
from profile import *
from photos import *
from download import *

import csv
import datetime
import json
import os
import time
import urllib.request
from urllib.request import Request

# from profile.py
def createProfiles():
	to_process = {}
	num_users = 0
	for user in USER_LIST:
		ask = int(input("Extract profile of " + user + "? 1 for YES, 0 for NO: "))
		to_process[user] = ask
		if (ask == 1):
			num_users += 1
	cnt = 0
	if (num_users > 0):
		csv = open("profiles.csv", "w")
		csv.write(genHeader(HEADER_LIST2))
		for user in USER_LIST:
			if (to_process[user] == 1):
				getProfile(user, csv)
				cnt += 1
			print("createProfiles(): " + str(user) + " " + str(cnt) + "/" + str(num_users) + " done.")
		csv.close()
	else:
		print("You chose not to download any profiles.")

# from photos.py
def createPhotoIndividual():
	to_process = {}
	num_users = 0
	for user in USER_LIST:
		ask = int(input("Extract photo data (individual) for " + user + "? 1 for YES, 0 for NO: "))
		to_process[user] = ask
		if (ask == 1):
			num_users += 1
			if not os.path.exists(user):
				os.makedirs(user)
	cnt = 0
	if (num_users > 0):
		for user in USER_LIST:
			if (to_process[user] == 1):
				csv = open(user + "/" + user + ".csv", "w")
				csv.write(genHeader(HEADER_LIST1))
				getPhotoData(user, csv)
				csv.close()
				cnt += 1
				print("createPhotoIndividual(): " + str(user) + " " + str(cnt) + "/" + str(num_users) + " done.")
	else:
		print("You chose not to download any photo data.")

# from download.py, downloadPhotos()
def createDownload():
	to_process = {}
	num_users = 0
	for user in USER_LIST:
		ask = int(input("Download photos for " + user + "? 1 for YES, 0 for NO: "))
		to_process[user] = ask
		if (ask == 1):
			num_users += 1
			if not os.path.exists(user):
				os.makedirs(user)
	cnt = 0
	if (num_users > 0):
		for user in USER_LIST:
			if (to_process[user] == 1):
				downloadPhotos(user)
				cnt += 1
				print("createDownload(): " + str(user) + " " + str(cnt) + "/" + str(num_users) + " done.")
	else:
		print("You chose not to download any photos.")

# from download.py, updatePhotos()
def createDownloadFromDate(user):
	print("Welcome to createDownloadFromDate. You can choose a date and all the photos posted after that date will be added to the user's photo directory.")
	year = int(input("Enter a year: "))
	month = int(input("Enter a month: "))
	day = int(input("Enter a day: "))
	updatePhotos(user, year, month, day)

createProfiles()
createPhotoIndividual()
createDownload()
createDownloadFromDate('sgig')