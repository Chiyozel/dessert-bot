# coding: utf8

import twitter
from twitter import TwitterError

import csv
import sys
import json
import random
import os.path

def get_chemin(type):
	if type == "tweetsDessert" : return '/home/pi/twitterBots/dessert/tweetsDessert.csv'
	elif type == "sinceID" : return '/home/pi/twitterBots/dessert/sinceMentions.txt'
	elif type == "waifus" : return '/home/pi/twitterBots/dessert/waifusDessert.csv'

def process_status():
	try:
		twitter.post_tweet(pick_random_tweet())
	
	except IOError as e:
		print("Erreur de lecture du fichier csv.")
		
	except TwitterError as te:
		print("Erreur lors de l'envoi du statut\n" + te.content)
		

def pick_random_tweet():
	file = open(get_chemin('tweetsDessert'), 'rb')
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
	f = open(get_chemin('sinceID'), 'rb')
	sinceID = f.read()
	print("ID : " + sinceID)
	f.close()

	mentions = twitter.get_mentions(sinceID)
	mentions.reverse()

	for mention in mentions:
		if "#waifu" in mention['text'] :
			print("Ca contient waifu") #Debug
			dessert_waifu(mention)
		print ("Fin") #Debug

		fout = file(get_chemin('sinceID'), "w+b")
		fout.seek(0)
		fout.truncate()
		fout.write(str(mention['id']))
		fout.close()

def process_retweet():
	retour = twitter.search_tweet("le dessert")
	
	# print(json.dumps(retour, sort_keys=True, indent=4, separators=(',', ': ')))
	
	twitter.retweet_tweet(retour['statuses'][0]['id_str'])
	

def process_mps():
	print("Le footballeur")

#######
#	FONCTIONNALITES DESSERT
#######

def dessert_waifu(tweet):
	file = open(get_chemin('waifus'), 'rb')
	
	liste = map(tuple, csv.reader(file))

	file.close()
	nombreWaifus = len(liste)
	print("Nombre de waifus : {}".format(nombreWaifus))

	# On sélectionne l'indice de la ligne selon l'alias Twitter de l'utilisateur
	idSel = id_from_string(tweet['user']['screen_name']) % nombreWaifus

	print("Id sélectionné : {}".format(idSel))

	# Ici, le tuple waifu est sous la forme (Nom Dessert, Adresse dessert[, Media_id])
	waifuSelected = liste[idSel]
	print(len(waifuSelected))

	#if len(waifuSelected) <= 2: # S'il n'y a pas de media_id, on uploade l'image
	media_id = twitter.upload_photo("images/{}.jpg".format(idSel))
	#liste[idSel] += (media_id,)
	#save_csv(get_chemin('waifus'), liste)
	#else:
	#	media_id = waifuSelected[2]

	texteTweet = "@{} Votre waifu-dessert est : {} !".format(tweet['user']['screen_name'], waifuSelected[0])

	try :
		twitter.post_tweet(texteTweet, tweet['id'], media_id)

	except TwitterError as te:
		print("Erreur lors de l'envoi du statut\n" + te.content)

#######
#	UTILITAIRES DIVERS
#######

def save_csv(csv_path, liste):
	out = open(csv_path,'w')

	csv_out = csv.writer(out)

	for row in liste:
		csv_out.writerow(row)

def id_from_string(sentence):
	"""
	Retourne un identifiant "unique" selon la phrase passée en paramètre.

	sentence -- La chaîne de caractère dont nous allons générer un entier pseudo unique.
	"""

	retour = 0
	i = 1
	for c in sentence :
		retour += ord(c) * i
		i += 1

	return retour
