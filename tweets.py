# coding: utf8

import twitter
from twitter import TwitterError

import csv
import sys
import json
import random

def process_status():
	try:
		#print(pick_random_tweet())
		twitter.post_tweet(pick_random_tweet())
		#twitter.post_photo("LE DAYUM.", "images/dessertdayum.png")
	
	except IOError as e:
		print("Erreur de lecture du fichier csv.")
		
	except TwitterError as te:
		print("Erreur de post du statut.\n" + te.content)
		
	
def pick_random_tweet():
	file = open('tweetsDessert.csv', 'rb')
	liste = map(tuple, csv.reader(file))
	
	somme_probas = sum([int(temp[1]) for temp in liste])
	pif = random.randint(1,somme_probas)
	
	compteur = 0
	for message, proba in liste:
		if compteur <= pif and pif <= (compteur + int(proba)):
			return message
		else:
			compteur += int(proba)
	
	return "LE DESSERT. REER"
	
def process_mentions():
	print("Oui")
	
def process_mps():
	print("Le footballeur")
