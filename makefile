# Make file for the MTG scraping project
all: mtg

# Execute the MTG crawler to extract the data connected to MTG cards
mtg:
	scrapy crawl MTG -o mtgCards.json -L INFO

bac:
	mv mtgCards.json mtgCards.json.bac
