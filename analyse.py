#!/usr/bin/env python

import json
import datetime
from numpy import swapaxes
from matplotlib import pyplot as plt
from operator import itemgetter

today = datetime.date(2015, 8, 7)
therosReleaseDate = datetime.date(2013, 9, 27)
therosBlock = ['Theros', 'Born of the Gods', 'Journey into Nyx']
ravnicaReleaseDate = datetime.date(2012, 10, 5)
ravnicaBlock = ['Return to Ravnica', 'Gatecrash', "Dragon's Maze"]

def loadData(fileName="mtgCards.json"):
    return json.loads(open(fileName).read())

def plot(cardList, startDay, endDay=today):
    startIndex = (startDay-today).days-1
    endIndex = (endDay-today).days-1
    for card in cardList:
        data = swapaxes(card["priceHistory"],0,1)
        dateStamps = [datetime.datetime.fromtimestamp(d / 1e3) for d in data[0]]
        plt.plot(dateStamps[startIndex:endIndex],data[1][startIndex:endIndex])
    plt.show()

def boxPlot(cardList, dates):
    plt.boxplot([values(data, date) for date in dates])
    locs, labels = plt.xticks(range(1, len(dates)+1), dates)
    plt.setp(labels, rotation=45)
    #plt.gca().set_yscale('log')
    plt.show()

def values(cardList, date):
    index = (date-today).days-1
    return [card["priceHistory"][index][1] for card in cardList]

def filter(cardList, field, values):
    return [card for card in cardList if card[field] in values]

def filterCutof(cardList, minMaxValue):
    return [card for card in cardList \
            if max(swapaxes(card["priceHistory"],0,1)[1]) >= minMaxValue]

def printByValue(CardList):
    print "\n".join([card["name"]+": "+card["currentValue"] for card in sorted(CardList, key=itemgetter('currentValue'))])

if __name__ == "__main__":
    data = loadData()

    printByValue(filter(data, "rarety", ['(U)']))

    data = filter(data, "rarety", ['(M)', '(R)'])
    #data = filter(data, "set", therosBlock)
    #data = filter(data, "set", ravnicaBlock)
    data = filter(data, "set", ["Return to Ravnica"])
    #data = filterCutof(data, 1)
    #plot(data, ravnicaReleaseDate)

    boxPlot(data, [(today-datetime.timedelta(days=30*i)) for i in range(30,0,-1)])
