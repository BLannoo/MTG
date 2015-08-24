# Make file for the MTG scraping project

all: scrape

# Execute the MTG crawler to extract the data connected to MTG cards
scrape:
	scrapy crawl MTG -o mtgCards.json -L INFO 

# create a backup of the data
bac:
	mv mtgCards.json mtgCards.bac
