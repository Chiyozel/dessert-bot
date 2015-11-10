# coding: utf8

import twitter
import textwrap
from twitter import TwitterError
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import csv
import sys
import json
import random
import os.path

def get_chemin(type):
	if type == "tweetsDessert" : return '/home/pi/twitterBots/dessert/tweetsDessert.csv'
	elif type == "sinceID" : return '/home/pi/twitterBots/dessert/sinceMentions.txt'
	elif type == "waifus" : return '/home/pi/twitterBots/dessert/waifusDessert.csv'
	elif type == "path" : return '/home/pi/twitterBots/dessert'
	elif type == "fonds" : return '/home/pi/twitterBots/dessert/fondsDessert.csv'

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
	retour = twitter.search_tweet("\"le dessert\"")
	
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

	media_id = twitter.upload_photo("{}/images/{}.jpg".format(get_chemin("path"), idSel))

	texteTweet = "@{} Votre waifu-dessert est : {} !".format(tweet['user']['screen_name'], waifuSelected[0])

	try :
		twitter.post_tweet(texteTweet, tweet['id'], media_id)

	except TwitterError as te:
		print("Erreur lors de l'envoi du statut\n" + te.content)

def parle_avec_dessert(tweet):
	file = open(get_chemin('fonds'), 'rb')
	
	liste = map(tuple, csv.reader(file))

	file.close()
	nombreFondsDessert = len(liste)

	# Ici, le tuple sélectionné sera sous la forme :
	# (X début, Y début, X fin, Y fin, taille, caractères max par ligne, nom du fond, R, G, B, nom de la police utilisée)

	fond = liste[random.randint(1, nombreFondsDessert-1)]

	image = gen_image(fond, "Enlève ta culotte, je suis pilote.")

	image.save(get_chemin("path") + '/images/essai.jpg')

#######
#	UTILITAIRES DIVERS
#######

def save_csv(csv_path, liste):
	out = open(csv_path,'w')

	csv_out = csv.writer(out)

	for row in liste:
		csv_out.writerow(row)

def gen_image(tuple, texte, v_cent = True, h_cent = True):
	img = Image.open("{}/images/{}".format(get_chemin("path"),tuple[6]))
	draw = ImageDraw.Draw(img)

	texte = texte.decode('utf-8')

	# font = ImageFont.truetype(<font-file>, <font-size>)
	font = ImageFont.truetype("{}/fonts/{}".format(get_chemin("path"), tuple[10]), int(tuple[4]), encoding="utf-8")
	
	# lines = [unicode(temp1, errors='replace') for temp1 in textwrap.wrap(texte, width=int(tuple[5]))]
	lines = textwrap.wrap(texte, width=int(tuple[5]))

	print(lines)
	if(v_cent) : # Si le texte est centré verticalement
		hauteurTotale = sum(h for l, h in [draw.textsize(temp.encode('utf-8')) for temp in lines])
		#hauteurTotale = 200
		offset = (int(tuple[1]) + int(tuple[3])) / 2 - (hauteurTotale / 2)
	else :
		offset = 0

	for line in lines:
		largeur, hauteur = font.getsize(line)

		if(h_cent) : # Si le texte doit être centré horizontalement
			x = (int(tuple[2]) + int(tuple[0])) / 2 - (largeur / 2)
		else :
			x = int(tuple[0])

		y = offset

		offset += hauteur
		# draw.text((x, y),"Sample Text",(r,g,b))
		draw.text((x, y), line, (int(tuple[7]),int(tuple[8]),int(tuple[9])), font=font)

	return img


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
