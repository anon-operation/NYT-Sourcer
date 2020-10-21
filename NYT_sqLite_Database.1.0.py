import sqlite3
from sqlite3 import Error
import pandas as pd
from pandas import DataFrame
import numpy as np
import pickle
import datetime



class Article:
    def __init__(self):
        self.sources = {}
        return;

class StoryMetadata:
    def __init__(self):
        self.pubDate = ""
        self.author = []
        self.section = ""
        self.url = ""
        self.sources = {}
        return;

def load_NYT_data():
    with open(totalFileName,'rb') as handle:
        unserialized_data = pickle.load(handle)
    nameTallylist = []
    print("Name", "Section", "Url", "Date", "Title", "Count","Type",sep =",",file=outfile)
    for key in unserialized_data:
        try:
            article=unserialized_data[key]
            title=key.replace(",", " ")
            #title=key
            section=article.section
            url=article.url
            author=article.author
            date=str(article.pubDate)
            fixedDate=date[:-6]
            count=1
            innerList=[section,url,author,date]
            sources=article.sources
            NLTKs=sources['NLTK']
            highs=sources['highAttributes']
            lows=sources['lowAttributes']
            knowns=sources['knownNames']
            for name in NLTKs:
                lower=name.lower()
                print(lower, section, url, fixedDate, title, count,"nltk", sep=",",file=outfile)

            for name in highs:
                lower=name.lower()
                print(lower, section, url, fixedDate, title, count,"high",sep=",",file=outfile)

            for name in lows:
                lower=name.lower()
                print(lower, section, url, fixedDate, title, count,"low",sep=",",file=outfile)

            for name in knowns:
                lower=name.lower()
                print(lower, section, url, fixedDate, title, count,"known",sep=",",file=outfile)


        except:
            tryVar=0
    outfile.flush()
    outfile.close()

    df=pd.read_csv('toDatabaseData.csv', sep=',')

    return df

sqlfilename = "NYT.sqlite"

connex = sqlite3.connect(sqlfilename)
curs = connex.cursor()

try:
    curs.execute('''CREATE TABLE ARTICLES
                ([generated_id] INTEGER PRIMARY KEY, [Name] text, [Section] text, [Url] text, [Date] text, [Title] text, [Count] integer, [Type] text)''')

except:
    print("Table already exists. Proceed :)")
    
connex.commit()

Q1=input("Do you want to append to the database? ")
if Q1.lower()[0]=="y":
    filename=input("Type the pickle file you want to add. You don't need to add .pickle: ")

totalFileName=(filename+".pickle")
outfile = open("toDatabaseData.csv", "w", encoding='utf-8')

data=load_NYT_data()
print(data)

data.to_sql('ARTICLES', connex, if_exists='append', index = False)
#curs.execute('''INSERT INTO ARTICLES (Name, Section, Url, Date, Title, Count)''')

dataFrame = DataFrame(curs.fetchall(), columns=['Name', 'Section', 'Url', 'Date', 'Title', 'Count'])
print(dataFrame)

