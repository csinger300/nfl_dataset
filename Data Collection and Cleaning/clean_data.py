########## This file will contain all the Python code you utilized to clean your raw data ##########
import pymysql
import csv
from pprint import pprint

def csv_cleaner1(fileName):
    with open(fileName, 'r', encoding = 'utf8') as f:
        finallist = []
        dict_reader = csv.DictReader(f, delimiter = ",", quotechar = '"')
        for adict in dict_reader:
            bdict = {}
            bdict['playerId'] = adict['playerId']
            bdict['draft'] = adict['draft']
            bdict['round'] = 0 if adict['round'] == '' else int(float(adict['round']))
            bdict['pick'] = adict['pick']
            bdict['draftTradeValue'] = adict['draftTradeValue']
            bdict['draftTeam'] = adict['draftTeam']
            bdict['position'] = adict['position']
            bdict['teamId'] = adict['teamId']
            bdict['nameFull'] = adict['nameFull']
            bdict['collegeId'] = adict['collegeId']
            bdict['college'] = adict['college']
            bdict['heightInches'] = 0 if adict['heightInches'] == '' else adict['heightInches']
            bdict['weight'] = 0 if adict['weight'] == '' else adict['weight']
            bdict['homeCountry'] = 'NA' if adict['homeCountry'] == '' else adict['homeCountry']
            finallist.append(bdict)
    with open("clean1.csv", "w") as fout:
        writer = csv.DictWriter(fout, fieldnames = finallist[0].keys(), lineterminator = '\n')
        writer.writeheader()
        writer.writerows(finallist)
csv_cleaner1('Raw Data/raw1.csv')

def csv_cleaner2(fileName):
    with open(fileName, 'r', encoding = 'utf8') as f:
        finallist = []
        dict_reader = csv.DictReader(f, delimiter = ",", quotechar = '"')
        for adict in dict_reader:
            adict['fumTurnover'] = True if (adict['fumTurnover'] != "" and float(adict['fumTurnover']) == 1.0) else False
            adict['fumNull'] = True if float(adict['fumNull']) == 1.0 else False
            finallist.append(adict)
    with open("clean2.csv", "w") as fout:
        writer = csv.DictWriter(fout, fieldnames = finallist[0].keys(), lineterminator = '\n')
        writer.writeheader()
        writer.writerows(finallist)
csv_cleaner2('Raw Data/raw2.csv')

def csv_cleaner3(fileName):
    with open(fileName, 'r', encoding = 'utf8') as f:
        finallist = []
        dict_reader = csv.DictReader(f, delimiter = ",", quotechar = '"')
        for adict in dict_reader:
            bdict = {}
            bdict['receiverId'] = adict['receiverId']
            bdict['playId'] = adict['playId']
            bdict['teamId'] = adict['teamId']
            bdict['playerId'] = adict['playerId']
            bdict['recPosition'] = adict['recPosition']
            bdict['recYards'] = adict['recYards']
            bdict['rec'] = True if int(adict['rec']) == 1 else False
            bdict['result'] = 'loss/no gain' if int(adict['recYards']) <= 0 else 'gain'
            finallist.append(bdict)
    with open("clean3.csv", "w") as fout:
        writer = csv.DictWriter(fout, fieldnames = finallist[0].keys(), lineterminator = '\n')
        writer.writeheader()
        writer.writerows(finallist)
csv_cleaner3("Raw Data/raw3.csv")

def csv_cleaner4(fileName):
    with open(fileName, 'r', encoding = 'utf8') as f:
        finallist = []
        dict_reader = csv.DictReader(f, delimiter = ",", quotechar = '"')
        for adict in dict_reader:
            bdict = {}
            bdict['sackId'] = adict['sackId']
            bdict['playId'] = adict['playId']
            bdict['teamId'] = adict['teamId']
            bdict['playerId'] = adict['playerId']
            bdict['sackPosition'] = adict['sackPosition']
            bdict['sackYards'] = adict['sackYards']
            bdict['sackEnd'] = adict['sackEnd']
            finallist.append(bdict)
    with open("clean4.csv", "w") as fout:
        writer = csv.DictWriter(fout, fieldnames = finallist[0].keys(), lineterminator = '\n')
        writer.writeheader()
        writer.writerows(finallist)
csv_cleaner4('Raw Data/raw4.csv')

def csv_cleaner5(fileName):
    with open(fileName, 'r', encoding = 'utf8') as f:
        finallist = []
        dict_reader = csv.DictReader(f, delimiter = ",", quotechar = '"')
        for adict in dict_reader:
            bdict = {}
            bdict['playerId'] = adict['playerId']
            bdict['nameFull'] = adict['nameFull']
            bdict['position'] = 'NA' if adict['position'] == '' else adict['position']
            bdict['college'] = adict['college']
            bdict['heightInches'] = 0 if adict['heightInches'] == '' else adict['heightInches']
            bdict['weight'] = 0 if adict['weight'] == '' else adict['weight']
            finallist.append(bdict)
    with open("clean5.csv", "w") as fout:
        writer = csv.DictWriter(fout, fieldnames = finallist[0].keys(), lineterminator = '\n')
        writer.writeheader()
        writer.writerows(finallist)
csv_cleaner5('Raw Data/raw5.csv')

def csv_cleaner6(fileName):
    with open(fileName, 'r', encoding = 'utf8') as f:
        finallist = []
        dict_reader = csv.DictReader(f, delimiter = ",", quotechar = '"')
        for adict in dict_reader:
            bdict = {}
            bdict['interceptionId'] = adict['interceptionId']
            bdict['playId'] = adict['playId']
            bdict['teamId'] = adict['teamId']
            bdict['playerId'] = adict['playerId']
            bdict['intPosition'] = adict['intPosition']
            bdict['intYards'] = adict['intYards']
            bdict['intTd'] = True if int(adict['intTd']) == 1 else False
            finallist.append(bdict)
    with open("clean6.csv", "w") as fout:
        writer = csv.DictWriter(fout, fieldnames = finallist[0].keys(), lineterminator = '\n')
        writer.writeheader()
        writer.writerows(finallist)
csv_cleaner6('Raw Data/raw6.csv')

connection = pymysql.connect(host = 'localhost', user = 'root', password = 'bailey69', db = 'NFLData', charset = "utf8mb4", cursorclass = pymysql.cursors.Cursor)
cursor = connection.cursor()

cursor.execute('DROP DATABASE IF EXISTS NFLData;')
cursor.execute('CREATE DATABASE NFLData;')
cursor.execute('USE NFLData;')

draftTable = 'CREATE TABLE draftTable (playerId int, draft int, round int, pick int, draftTradeValue float, draftTeam varchar(50), position varchar(50), teamId int, nameFull varchar(255), collegeId int, college varchar(255), heightInches float, weight float, homeCountry varchar(50));'
fumbleTable = 'CREATE TABLE fumbleTable (fumId int, playId int, teamId int, playerId int, fumPosition varchar(50), fumType varchar(50), fumOOB int, fumTurnover varchar(50), fumNull varchar(50));'
receiverTable = 'CREATE TABLE receiverTable (receiverId int, playId int, teamId int, playerId int, recPosition varchar(50), recYards int, rec varchar(50), result varchar(50));'
sackTable = 'CREATE TABLE sackTable (sackId int, playId int, teamId int, playerId int, sackPosition varchar(50), sackYards int, sackEnd varchar(50));'
playerTable = 'CREATE TABLE playerTable (playerId int, nameFull varchar(255), position varchar(50), college varchar(255), heightInches float, weight float);'
interceptionTable = 'CREATE TABLE interceptionTable (interceptionId int, playId int, teamId int, playerId int, intPosition varchar(255), intYards int, intTd varchar(50));'

cursor.execute(draftTable)
cursor.execute(fumbleTable)
cursor.execute(receiverTable)
cursor.execute(sackTable)
cursor.execute(playerTable)
cursor.execute(interceptionTable)

with open('clean1.csv') as f:
    csv_data1 = csv.reader(f, delimiter = ',', quotechar = '"')
    reader_list = list(csv_data1)
    for row in reader_list[1:]:
        cursor.execute('INSERT INTO draftTable VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', row)

with open('clean2.csv') as f:
    csv_data2 = csv.reader(f, delimiter = ',', quotechar = '"')
    reader_list = list(csv_data2)
    for row in reader_list[1:]:
        cursor.execute('INSERT INTO fumbleTable VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);', row)

with open('clean3.csv') as f:
    csv_data3 = csv.reader(f, delimiter = ',', quotechar = '"')
    reader_list = list(csv_data3)
    for row in reader_list[1:]:
        cursor.execute('INSERT INTO receiverTable VALUES(%s, %s, %s, %s, %s, %s, %s, %s);', row)

with open('clean4.csv') as f:
    csv_data4 = csv.reader(f, delimiter = ',', quotechar = '"')
    reader_list = list(csv_data4)
    for row in reader_list[1:]:
        cursor.execute('INSERT INTO sackTable VALUES(%s, %s, %s, %s, %s, %s, %s);', row)

with open('clean5.csv') as f:
    csv_data5 = csv.reader(f, delimiter = ',', quotechar = '"')
    reader_list = list(csv_data5)
    for row in reader_list[1:]:
        cursor.execute('INSERT INTO playerTable VALUES(%s, %s, %s, %s, %s, %s);', row)

with open('clean6.csv') as f:
    csv_data6 = csv.reader(f, delimiter = ',', quotechar = '"')
    reader_list = list(csv_data6)
    for row in reader_list[1:]:
        cursor.execute('INSERT INTO interceptionTable VALUES(%s, %s, %s, %s, %s, %s, %s);', row)

connection.commit()
cursor.close()


