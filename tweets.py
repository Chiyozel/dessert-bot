# coding: utf8

import twitter
from twitter import TwitterError

import csv
import sys
import json
import random

chemin['tweetsDessert'] = '/home/pi/twitterBots/dessert/tweetsDessert.csv'
chemin['sinceID'] = '/home/pi/twitterBots/dessert/sinceID.txt'
chemin['waifus'] = '/home/pi/twitterBots/dessert/waifuDessert.csv'

def process_status():
	try:
		#print(pick_random_tweet())
		twitter.post_tweet(pick_random_tweet())
		#twitter.post_photo("LE DAYUM.", "images/dessertdayum.png")
	
	except IOError as e:
		print("Erreur de lecture du fichier csv.")
		
	except TwitterError as te:
		print("Erreur lors de l'envoi du statut\n" + te.content)
		
	
def pick_random_tweet():
	file = open(chemin['tweetsDessert'], 'rb')
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
	file = open(chemin['sinceID'], 'rw')
	sinceID = file.read()
	mentions = twitter.get_mentions(sinceID)

	mentions.reverse()

	for mention in mentions:
		file.write(mention['id'])
		if "#waifu" in mention['text']:
			dessert_waifu(mention)

	return retour
	
def process_retweet():
	retour = twitter.search_tweet("le dessert")
	
	# print(json.dumps(retour, sort_keys=True, indent=4, separators=(',', ': ')))
	
	twitter.retweet_tweet(retour['statuses'][0]['id_str'])
	
def process_mps():
	print("Le footballeur")

def dessert_waifu(tweet):
	file = open(chemin['waifus'], 'rb')
	
	nombreWaifus = n = sum(1 for _ in file)
	liste = map(tuple, csv.reader(file))

	waifuSelected = liste[id_from_string(tweet['user']) % nombreWaifus]

	# TO-DO : Uploader l'image correspondante, et répondre à l'utilisateur

def id_from_string(sentence):
	"""
	Retourne un identifiant "unique" selon la phrase passée en paramètre.

	sentence -- La chaîne de caractère dont nous allons générer un entier pseudo unique.
	"""

	retour = 0
	i = 1
	for c in sentence :
		retour += ord(c) * i
		i++
