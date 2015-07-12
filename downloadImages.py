# coding: utf8

import urllib
import csv

file = open('/home/pi/twitterBots/dessert/waifusDessert.csv', 'rb')
liste = map(tuple, csv.reader(file))
i = 0
for dessert in liste :
	url = dessert[1][1:-1]
	print(url_fix(url))
	print("Téléchargement de l'image {} du dessert \"{}\" en cours à l'adresse : {}".format(i, dessert[0], url))
	urllib.urlretrieve(url, "images/{}.jpg".format(i))
	i += 1