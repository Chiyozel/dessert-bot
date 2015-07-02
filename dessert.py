# coding: utf8

import sys
import tweets
import time

def print_usage() :
	print("USAGE : python dessert.py [argument]\n\tstatut : Envoie le statut dessert\n\tmentions : Analyse les mentions\n\tmessages : Répond aux messages privés\n\tretweet : Retweete un tweet au hasard contenant \"LE DESSERT\"")
	

if len(sys.argv) != 2 :
	print_usage()
	sys.exit(0)
else:
	if sys.argv[1] == "statut":
		print("Post du statut débuté ({})".format(time.strftime("%c")))
		tweets.process_status()
		print("Post du statut complété.")
		
	elif sys.argv[1] == "mentions":
		print("Traitement des mentions en cours ({})".format(time.strftime("%c")))
		tweets.process_mentions()
		print("Traitement des mentions complété.")
		
	elif sys.argv[1] == "messages":
		print("Traitement des messages privés en cours ({})".format(time.strftime("%c")))
		tweets.process_mps()
		print("Traitement des messages privés complété.")
		
	elif sys.argv[1] == "retweet":
		print("Début du retweet en cours ({})".format(time.strftime("%c")))
		tweets.process_retweet()
		print("Tweet retweeté.")
		
	else:
		print_usage()
	
	
	