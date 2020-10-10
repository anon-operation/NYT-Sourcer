
outfile = open("nameDataFrame.csv", "w", encoding='utf-8')


########## Test change


import pickle
import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'firefox'


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

filename=""
totalFileName=filename+".pickle"
questionString=("The current database file is: "+ filename+". is that correct? " )
fileq=input(questionString)
if fileq.lower()[0]=="y":
    totalFileName=filename+".pickle"
    with open(totalFileName,'rb') as handle:
        unserialized_data = pickle.load(handle)
else:
    fileq2=input("Type the file name, without the .pickle at the end, you want to use. ")
    filename=fileq2
    totalFileName=filename+".pickle"
    with open(totalFileName,'rb') as handle:
        unserialized_data = pickle.load(handle)
    
#q0 = input("Do you want to see the saved dictionary of sources?  ")
#if q0.lower()[0]=="y":
#    print("The packed and unpacked data is:")
#    print()
#    for key in unserialized_data:
#        article=unserialized_data[key]
#        print(key, " , ", article.sources)
#        print()
q1=input("Do you want to tally the source data? ")
if q1.lower()[0]=="y":
    nameTallylist = []
    print("Name", ",", "Section",",","Url",",","Date",",","Title",",","Count",file=outfile)
    for key in unserialized_data:
        try:
            article=unserialized_data[key]
            #print(key)
            #print(article.sources)
            title=key.replace(",", " ")
            section=article.section
            url=article.url
            author=article.author
            date=article.pubDate
            count=1
            innerList=[section,url,author,date]
            sources=article.sources
            NLTKs=sources['NLTK']
            for name in NLTKs:
                #print("name in NLTKs are: ", name)
                lower=name.lower()
                print(lower, ",", section,",",url,",",date,",",title,",",count, file=outfile)
        except:
            print()
    outfile.flush()
    outfile.close()
    print("written to nameDataFrame.csv")
print("done")

q1_1=input("Do you want to graph the source data? ")
if q1_1.lower()[0]=="y":
    df=pd.read_csv('nameDataFrame.csv')
    print(df)

    df2=df.loc[df.duplicated(subset='Name ', keep=False), :]
    fig=px.bar(df2, x="Name ", y=" Count", color=" Section ",
            hover_data=[" Title ", " Url ", " Date "],
            title="Sources Tally")
    fig.show()

    
 
##            if lower not in nameTallydict.keys():
##                nameTallydict[lower]=1
##            elif lower in nameTallydict.keys():
##                prevVal = nameTallydict[lower]
##                newVal = (prevVal+1)
##                nameTallydict[lower]=newVal
##                
##q1_1=input("Do you want to comlex tally the source data? ")
##
####nameTallylist=[source name, ]
##
##if q1_1.lower()[0]=="y":
##    complexNameTallydict = {}
##    for key in unserialized_data:
##        article=unserialized_data[key]
##        section=article.topic
##        NLTKs=article.sources['NLTK']
##        innerDict[article]={section,date}
##        for name in NLTKs:
##            #print("keys in NLTKs are: ", name)
##            lower=name.lower()
##            nameTallydict[lower]=innerDict
##
##
##
##
##q2=input("Do you want to see the results? ")
##if q2.lower()[0]=="y":
##    print (nameTallydict)
##            
##df=pd.DataFrame(list(nameTallydict.items()),
##                columns = ['Name','# of articles using the name'])
##
##moreThanOne = df[df["# of articles using the name"]>1]
###print(moreThanOne)
##
##
##fig = px.bar(moreThanOne,
##             y="# of articles using the name",
##             x="Name")
###fig.show()
###print(pio.renderers.default)
##
