import csv
import json
import os

def main():
    readCities()

def readCities():
    with open('Cities.csv', newline='') as citiesFile:
        citiesReader = csv.reader(citiesFile, delimiter=';', quotechar='|')
        next(citiesReader)
        for city in citiesReader:
            readCity(city)

def readCity(city):
    state = city[2].replace('\'','').replace(' ','_').lower()
    coords = city[5]
    filename = 'temp.json'
    cmd = "twint -s coronavirus -g=\""+coords+",4km\" -o "+filename+" --json --since \"2020-01-01 00:00:00\""
    os.system(cmd)
    transferTemp(state)

def transferTemp(state):
    if not os.path.exists('temp.json'):
        return
    file = open('temp.json', 'r')
    data = file.read().split('\n')
    lines = []
    for row in data:
        try:
            tweet = json.loads(row)
            id = tweet['id']
            date = tweet['date']
            body = formatBody(tweet['tweet'])
            lines.append(state+','+date+','+body)
        except:
            continue
    os.remove('temp.json')
    writeLines(state, lines)
    file.close()

def formatBody(body):
    clean = body.replace('\n','').replace(',','')
    stripped = (c for c in clean if 0 < ord(c) <127)
    tokens = ''.join(stripped).split(' ')
    cleaned = (token for token in tokens if len(token) < 15)
    return ' '.join(cleaned)

def writeLines(state, lines):
    file = open('FilteredTweets/'+state+'.csv','a')
    for line in lines:
        file.write(line+'\n')
    file.close()


if __name__ == '__main__':
    main()