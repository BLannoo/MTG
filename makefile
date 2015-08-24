# Make file for the MTG scraping project

all: mtgCards.json
bac: mtgCards.bac

# Execute the MTG crawler to extract the data connected to MTG cards
mtgCards.json:
	scrapy crawl MTG -o $@ -L INFO 

# create a backup of the data
mtgCards.bac:
	mv mtgCards.json mtgCards.bac
