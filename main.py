from constants import *
from functions import *
from user_list import USER_LIST
from profile import *
from photos import *

import csv
import datetime
import json
import time
import urllib.request
from urllib.request import Request

def createProfiles():
	to_process = {}
	for user in USER_LIST:
		ask = int(input("Extract profile of " + user + "? 1 for YES, 0 for NO: "))
		to_process[user] = ask
	if (num_users > 0):
		csv = open("profiles.csv", "w")
		csv.write(genHeader(HEADER_LIST2))
		for user in USER_LIST:
			if (to_process[user] == 1):
				getProfile(user, csv)
		csv.close()

def createPhotoIndividual():
	to_process = {}
	for user in USER_LIST:
		ask = int(input("Extract photo data for " + user + "? 1 for YES, 0 for NO: "))
		to_process[user] = ask
	if (num_users > 0):
		for user in USER_LIST:
			csv = open(user + ".csv", "w")
			csv.write(genHeader(HEADER_LIST1))
			getPhotoData(user, csv)
			csv.close()

def createPhotoCombined():
	to_process = {}
	for user in USER_LIST:
		ask = int(input("Extract photo data for " + user + "? 1 for YES, 0 for NO: "))
		to_process[user] = ask
	if (num_users > 0):
		csv = open("combined.csv", "w")
		csv.write(genHeader(HEADER_LIST1))
		for user in USER_LIST:
			getPhotoData(user, csv)
		csv.close()

createProfiles()
createPhotoIndividual()
createPhotoCombined()