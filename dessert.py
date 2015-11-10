#!/usr/bin/python
# coding: utf8

import sys
import tweets
import time

def print_usage() :
	print("USAGE : python dessert.py [argument]\n\t-s : Envoie le statut dessert\n\t-m : Analyse les mentions\n\t-mp : Répond aux messages privés\n\t-r : Retweete un tweet au hasard contenant \"LE DESSERT\"")
	

if len(sys.argv) != 2 :
	print_usage()
	sys.exit(0)
else:
	if sys.argv[1] == "-s":
		print("Post du statut débuté ({})".format(time.strftime("%c")))
		tweets.process_status()
		print("Post du statut complété.")
		
	elif sys.argv[1] == "-m": 
		print("Traitement des mentions en cours ({})".format(time.strftime("%c")))
		tweets.process_mentions()
		print("Traitement des mentions complété.")
		
	elif sys.argv[1] == "-mp":
		print("Traitement des messages privés en cours ({})".format(time.strftime("%c")))
		tweets.process_mps()
		print("Traitement des messages privés complété.")
		
	elif sys.argv[1] == "-r":
		print("Début du retweet en cours ({})".format(time.strftime("%c")))
		tweets.process_retweet()
		print("Tweet retweeté.")

	elif sys.argv[1] == "-t":
		print("Début de la phase de test de la génération d'une image en cours.")
		tweets.parle_avec_dessert("joj")
		print("Image générée.")
		
	else:
		print_usage()
	
	
	
