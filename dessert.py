# coding: utf8

import sys
import tweets

def print_usage() :
	print("USAGE : python dessert.py [argument]\n\tstatut : Envoie le statut dessert\n\tmentions : Analyse les mentions\n\tmessages : Répond aux messages privés")
	

if len(sys.argv) != 2 :
	print_usage()
	sys.exit(0)
else:
	if sys.argv[1] == "statut":
		print("Post du statut débuté")
		tweets.process_status()
		print("Post du statut complété.")
		
	elif sys.argv[1] == "mentions":
		print("Traitement des mentions en cours...")
		tweets.process_mentions()
		print("Traitement des mentions complété.")
		
	elif sys.argv[1] == "messages":
		print("Traitement des messages privés en cours...")
		tweets.process_mps()
		print("Traitement des messages privés complété.")
		
	else:
		print_usage()
	
	
	