# Dessert Bot v2

Un bot qui aime beaucoup le dessert.

## Installation

Pour faire fonctionner ce bot vous aurez besoin de : 
* Python >= 2.7
* clés API Twitter (consumer key, consumer secret key, token key et secret token key) avec les autorisations de lecture, d'écriture et d'accès aux messages privés(vous devez créer une app sur dev.twitter.com)
* de quoi launch le script périodiquement (cron)

Mettez vos clés API dans le fichier twitter_settings.py et sauvegardez. Le script s'occupe du reste.

## Utilisation 

Le syntaxe principale est : `python dessert.py [argument]`

Comment arguments disponibles, vous avez :
- `statut`, qui vous permettra tout simplement de poster un tweet
- `mention`, qui s'occupera de répondre aux mentions
- `messages`, qui s'occupera de répondre aux messages privés



