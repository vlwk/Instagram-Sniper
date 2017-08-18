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

def main():
	# combining everything together
	csv2 = open("profiles.csv", "w")
	csv_combined = open("combined.csv", "w")

	csv_combined.write(genHeader(HEADER_LIST1))
	csv2.write(genHeader(HEADER_LIST2)) # write header2 row to csv2 (all the user profiles)

	to_process = {}

	num_users = 0
	for user in USER_LIST:
		ask = int(input("Would you like to process " + user + "? 1 for YES, 0 for NO: "))
		to_process[user] = ask
		if (ask == 1):
			num_users += 1

	cnt = 0
	for user in USER_LIST:
		csv1 = open(user + ".csv", "w")
		csv1.write(genHeader(HEADER_LIST1)) # write header1 row to csv1 (each user)
		if (to_process[user] == 1):

			getProfile(user, csv2)
			print(user + " " + "csv2 done.")

			getPhotoData(user, csv1)
			print(user + " " + "csv1 done.")

			getPhotoData(user, csv_combined)
			print(user + " " + "csv_combined done.")

			cnt += 1
			print("USER: " + user + " DONE WITH EXTRACTION (" + str(cnt) + "/" + str(num_users) + ")")
		csv1.close()

	csv2.close()
	csv_combined.close()

main()