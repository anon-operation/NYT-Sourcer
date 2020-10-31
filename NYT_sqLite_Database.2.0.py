
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
    with open('theHistoricalData.pickle','rb') as handle:
        unserialized_data = pickle.load(handle)
    nameTallylist = []
    print("Name", "Section", "Url", "Date", "Title", "Count","Type",sep =",", file=outfile)
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
            HTML_1_NLTKs=sources['HTML_1']['NLTK']
            HTML_1_NER=sources['HTML_1']['NER']
            HTML_1_ORG=sources['HTML_1']['NER_ORGS']
            HTML_1_high=sources['HTML_1']['high']
            HTML_1_low=sources['HTML_1']['low']
            HTML_1_known=sources['HTML_1']['known']
            HTML_2_NLTKs=sources['HTML_BS']['NLTK']
            HTML_2_NER=sources['HTML_BS']['NER']
            HTML_2_ORG=sources['HTML_BS']['NER_ORGS']
            HTML_2_high=sources['HTML_BS']['high']
            HTML_2_low=sources['HTML_BS']['low']
            HTML_2_known=sources['HTML_BS']['known']
            for name in HTML_1_NLTKs:
                nameS=name.replace(",", " ")
                nameClean=" ".join(nameS.split())
                lower=nameClean.lower()
                print(lower, section, url, fixedDate, title, count,"nltk_method1", sep=",", file=outfile)

            for name in HTML_1_ORG:
                nameS=name.replace(",", " ")
                nameClean=" ".join(nameS.split())
                lower=nameClean.lower()
                print(lower, section, url, fixedDate, title, count,"organizations_method1",sep=",", file=outfile)

            for name in HTML_1_high:
                nameS=name.replace(",", " ")
                nameClean=" ".join(nameS.split())
                lower=nameClean.lower()
                print(lower, section, url, fixedDate, title, count,"high_method1",sep=",", file=outfile)


            for name in HTML_1_low:
                nameS=name.replace(",", " ")
                nameClean=" ".join(nameS.split())
                lower=nameClean.lower()
                print(lower, section, url, fixedDate, title, count,"low_method1",sep=",", file=outfile)

            for name in HTML_1_NER:
                nameS=name.replace(",", " ")
                nameClean=" ".join(nameS.split())
                lower=nameClean.lower()
                print(lower, section, url, fixedDate, title, count,"ner_method1",sep=",", file=outfile)

            for name in HTML_1_known:
                nameS=name.replace(",", " ")
                nameClean=" ".join(nameS.split())
                lower=nameClean.lower()
                print(lower, section, url, fixedDate, title, count,"known_method1",sep=",", file=outfile)
                
            for name in HTML_2_NLTKs:
                nameS=name.replace(",", " ")
                nameClean=" ".join(nameS.split())
                lower=nameClean.lower()
                print(lower, section, url, fixedDate, title, count,"nltk_method2", sep=",", file=outfile)

            for name in HTML_2_ORG:
                nameS=name.replace(",", " ")
                nameClean=" ".join(nameS.split())
                lower=nameClean.lower()
                print(lower, section, url, fixedDate, title, count,"organizations_method2",sep=",", file=outfile)

            for name in HTML_2_high:
                nameS=name.replace(",", " ")
                nameClean=" ".join(nameS.split())
                lower=nameClean.lower()
                print(lower, section, url, fixedDate, title, count,"high_method2",sep=",", file=outfile)


            for name in HTML_2_low:
                nameS=name.replace(",", " ")
                nameClean=" ".join(nameS.split())
                lower=nameClean.lower()
                print(lower, section, url, fixedDate, title, count,"low_method2",sep=",", file=outfile)

            for name in HTML_2_NER:
                nameS=name.replace(",", " ")
                nameClean=" ".join(nameS.split())
                lower=nameClean.lower()
                print(lower, section, url, fixedDate, title, count,"ner_method2",sep=",", file=outfile)


            for name in HTML_2_known:
                nameS=name.replace(",", " ")
                nameClean=" ".join(nameS.split())
                lower=nameClean.lower()
                print(lower, section, url, fixedDate, title, count,"known_method2",sep=",", file=outfile)

        except:
            blank=0
    outfile.flush()
    outfile.close()

    df=pd.read_csv('toDatabaseData.csv', sep=',')

    return df

sqlfilename = "DB.sqlite"

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
    #filename=input("Type the pickle file you want to add. You don't need to add .pickle: ")
    filename="theHistoricalData"
totalFileName=(filename+".pickle")
outfile = open("toDatabaseData.csv", "w", encoding='utf-8')

data=load_NYT_data()
print(data)

data.to_sql('ARTICLES', connex, if_exists='append', index = False)
#curs.execute('''INSERT INTO ARTICLES (Name, Section, Url, Date, Title, Count, Type)''')
##
##dataFrame = DataFrame(curs.fetchall(), columns=['Name', 'Section', 'Url', 'Date', 'Title', 'Count', 'Type'])
##print(dataFrame)
##
##
