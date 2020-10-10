#method 1 from: https://stackoverflow.com/questions/20290870/improving-the-extraction-of-human-names-with-nltk/24119115

## Git test
################### pREREQS ##############################
import requests
import json
import pickle

class StoryMetadata:
    def __init__(self):
        self.pubDate = ""
        self.author = []
        self.section = ""
        self.url = ""
        self.sources = {}
        return;
    
class Article:
    def __init__(self):
        self.sources = {}
        return;

import http.cookiejar
import nltk
import re
import urllib

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
from nameparser.parser import HumanName

attributions = ["said","says","according","explains","explained","agreed"]
High_attributions = ["said","says","according","explains","explained", "explain"]
Low_attributions = ["recalls","recalled","thinks","think","describe","agreed","agrees","describes","described","points""pointed","point","indicates","indicate","indicated"]

Highnamelist = []
Lownamelist = []
namelist = []
KnownNames = []
KnownNames_singles = []
From_KnownNames = []
NYTdict = {} ##{ articleTitle:ArticleObject }

KnownNamesDict = {}  ##{'letter':[list of names starting with that letter]}


def get_human_names(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)
    person_list = []
    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1: #avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []

    return (person_list)

def find_prev_next(elem, elements):
    P = None
    N = None
    item = elem
    index = elements.index(elem)
    if index > 0:
        P = elements[index -1]
    if index < (len(elements)-1):
        N = elements[index +1]
    if index < (len(elements)-1):
        NN = elements[index +2]
    if index < (len(elements)-1):
        NNN = elements[index +3]
    if index < (len(elements)-1):
        NNNN = elements[index +4]
    return (P, item, N)

def find_prev(elem, elements):
    P = None
    item = elem
    index = elements.index(elem)
    if index > 0:
        P = elements[index -1]
    return (P, item)

def find_next(elem, elements):
    N = None
    item = elem
    index = elements.index(elem)
    if index < (len(elements)-1):
        N = elements[index +1]
    return (item, N)




def couples(elem, elements):
    P = None
    N = None
    item = elem
    index = elements.index(elem)
    if index > 0:
        P = elements[index -1]
    if index < (len(elements)-1):
        N = elements[index +1]
    if index < (len(elements)-1):
        NN = elements[index +2]
    return (P, item, N,NN)


####
KnownNamesDict={
    'a':[],
    'b':[],
    'c':[],
    'd':[],
    'e':[],
    'f':[],
    'g':[],
    'h':[],
    'i':[],
    'j':[],
    'k':[],
    'l':[],
    'm':[],
    'n':[],
    'o':[],
    'p':[],
    'q':[],
    'r':[],
    's':[],
    't':[],
    'u':[],
    'v':[],
    'w':[],
    'x':[],
    'y':[],
    'z':[]}
def alphabetize(name):
    abcs = ["a","b","c","d","e","f","g","h",
            "i","j","k","l","m","n","o","p",
            "q","r","s","t","u","v","w","x",
            "y","z"]
    global KnownNamesDict
    for letter in abcs:
        if name.lower()[0]==letter:
            if name in letter:
                 print("We've seen ", name, " before'")
            else:
                toapplist = KnownNamesDict[letter]
                toapplist.append(name)
                KnownNamesDict[letter] = toapplist
    return()

##################### Incorporate previous data  ########################

with open('filename.pickle','rb') as handle:
    unserialized_data = pickle.load(handle)
    
q0 = input("Do you want to see the previously saved dictionary of sources?  ")
if q0.lower()[0]=="y":
    print("The packed and unpacked data is:")
    print()
    for key in unserialized_data:
        article=unserialized_data[key]
        print(key, " , ", article.section," , ", article.sources)
        print()


q0_1 = input("Do you want to add to the previously saved dictionary of sources?  ")
if q0.lower()[0]=="y":
    topStoriesDict = unserialized_data
    checkList=[]
    for key in topStoriesDict:
        checkList.append(key)
    print("The known titles are: ")
    print(checkList)
else:
    topStoriesDict = {} ##{headlin:StoryMetadata object}
    checkList=[]


#print("topStoriesDict is: ", topStoriesDict)
###########################################################################################################
    

your_key =input("Enter your NYT API key. ")
getReq=("https://api.nytimes.com/svc/topstories/v2/home.json?api-key="+your_key)
result = requests.get(getReq)
#print(result.status_code) #200 is all good
dictMain = json.loads(result.text)
numOfArticles=dictMain['num_results']

#print("Today there are ",numOfArticles, " top stories on the NYT front page.")
#print()
for i in range(0,(int(numOfArticles))):
    ArticleDict=dictMain['results'][i]
    title=ArticleDict['title']
    date=ArticleDict['published_date']
    author=ArticleDict['byline']
    authorsplit=author.split(",")
    section=ArticleDict['section']
    url=ArticleDict['url']
    for i in authorsplit:
            if "and" in i:
                secondsplit=i.split(" and ")
                del authorsplit[-1]
                for x in secondsplit:
                    authorsplit.append(x)
    for z in range(0,len(authorsplit)):
        looking=authorsplit[z]
        if "By " in looking:
            nonby=looking.replace('By ','')
            authorsplit[z]=nonby
    if title not in checkList:
        #print(title, " is a new addition to the dictionary.")
###########################################################                    
        new=StoryMetadata()
        new.pubDate=date
        new.section=section
        new.url=url
        new.author=authorsplit
        topStoriesDict[title]=new



########################################MAIN BODY###################

counter=0
TEXT = []
TEXT.clear()
ALLFULLTEXTS = []
for key in topStoriesDict:
    current=topStoriesDict[key]
    if key not in checkList:
        theArticleTitle=key
        url=current.url
        #print(url)
        #print()
    ####
        try:
            cj=http.cookiejar.MozillaCookieJar()
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

            opener.addheaders = [('User-agent','Mozilla/5.0')]

            webURL = url
            #print()
            #print(webURL)
            infile = opener.open(webURL)

            newpage = infile.read().decode('utf-8')
        #get articleTitle
            titlesplit=newpage.split("<title data-rh=")
            titleportion=titlesplit[1]
            hastitle=titleportion.split("</title>")
            istitle=hastitle[0]
            thetitle=istitle.split(">")
            title=thetitle[1]
            #print(title)
            #print()
            #print()
        #done getting article title// now build source dictionary
            thisArticlesSourcesDict={"NLTK":{},
                                     "highAttributes":{},
                                     "lowAttributes":{},
                                     "knownNames":{}}
            new=Article()

        ##############################
    ################################
            paragsplit = newpage.split("p class")
                #print()
                #print(paragsplit)

            wordyparags = paragsplit[2:]
            for parag in wordyparags:
                arrowsplit = parag.split(">")
                arrowsplitend = arrowsplit[1].split("<")
                TEXT.append(arrowsplitend[0])
            fulltext = ' '.join(TEXT)
            #print(counter,",",fulltext)
            #print("Something Happened...is Good.")
            text = fulltext
            names = get_human_names(text)
            nameCountiterate=0
    #####
##            print("Names being added from", key, " are: ")
##            for name in names:
##                print(name)
    #####
            
            for name in names:
                sourceNumber = ("source"+str(nameCountiterate))
                firname = str(HumanName(name).first)
                laname = str(HumanName(name).last)
                try:
                    alphabetize(firname)
                    alphabetize(laname)
                except Exception as e:
                    blankvar=0
                    #print()
                    #print("Either the first or last name is missing, so alphabetize failed. No big deal") 
                    #print(e)
                thisArticlesSourcesDict["NLTK"][name] = {
                    "sourceNumber":sourceNumber,
                    "firstName":HumanName(name).first,
                    "lastName":HumanName(name).last
                    }
                current.sources = thisArticlesSourcesDict
    ##                current.sources = new


                    ############################
    ##                print("NYTdict is now:")
    ##                for key in NYTdict:
    ##                    current=NYTdict[key]
    ##                    print(key, ",", current.sources)
    ##
    ##                print()
    ##                print()
    ##                #########
                nameCountiterate+=1
                ##################################################################### removes "Mr."s
            mrList=[]
            nonMrList=[]
            for name in thisArticlesSourcesDict["NLTK"]:
                if "Mr." in name:
                    mrList.append(name)
                if "Mr." not in name:
                    nonMrList.append(name)
                    
            #print("Mr. list is: ")
            #print(mrList)
            #print("The non Mr list is:")
            #print(nonMrList)

            for i in range(0, len(mrList)):
                name=mrList[i]
                theName=name.replace("Mr. ", "")
                mrList[i]=theName
            #print("Mr list is now: ", mrList)
            tASDict={}
            for name in thisArticlesSourcesDict["NLTK"]:
                if ("Mr." in name):
                    #print("################### this is the name. It should have Mr. ", theName)
                    demistered=name.replace("Mr.","")
                    #print("@@@@@@@ Now it shouldn't have thge mr:  ", demistered)
                    strung=' '.join(nonMrList)
                    #print("Collapsed list is: ", strung)
                    if demistered in strung:
                        placeHolder=0
                        #print(name, " is a repeat.")
                    else:
                        tASDict[name] = thisArticlesSourcesDict["NLTK"][name]
                        #print(name, "is not a repeat.")
                else:
                    tASDict[name]=thisArticlesSourcesDict["NLTK"][name]
                    #print(name, " never contained Mr. and is kept.")

            thisArticlesSourcesDict["NLTK"]=tASDict
            #print()
            #print("The updated dictionary is: ")
            #print(thisArticlesSourcesDict)
            #print()
               ####

            try:
                words = text.split(" ")
                for i in words:
                    nearby = find_prev_next(i, words)
                    for x in High_attributions:
                        if x in nearby:
                            joined = ' '.join(nearby)
                            if ((len(re.findall('([A-Z][a-z]+)', joined)))>1):
                                t = re.findall('([A-Z][a-z]+)', joined)
                                name = ' '.join(t)
                                Highnamelist.append(name)
                                    #print(namelist)
            except:
                blank=[]
            try:
                words = text.split(" ")
                for i in words:
                    nearby = find_prev_next(i, words)
                    for x in Low_attributions:
                        if x in nearby:
                            joined = ' '.join(nearby)
                            if ((len(re.findall('([A-Z][a-z]+)', joined)))>1):
                                t = re.findall('([A-Z][a-z]+)', joined)
                                name = ' '.join(t)
                                Lownamelist.append(name)
                                    #print(namelist)
            except:
                blank=[]


            try:
                words = text.split(" ")
                for i in words:
                    nearby = find_next(i, words)
                    for x in nearby:
                        letter = x.lower()[0]
                        namelisting = KnownNamesDict[letter]
                        if x in namelisting:
                            joined = ' '.join(nearby)
                            if ((len(re.findall('([A-Z][a-z]+)', joined)))>1):
                                t = re.findall('([A-Z][a-z]+)', joined)
                                name = ' '.join(t)
                                From_KnownNames.append(name)
            except:
                blank=[]
            seen = {}
            dupes = []
            for item in namelist:
                if item not in seen:
                    seen[item] = 1
                else:
                    if seen[item] == 1:
                        dupes.append(item)
                    seen[item] +=1




            uniquenames = list(set(namelist))
            highuniquenames = list(set(Highnamelist))
            lowuniquenames = list(set(Lownamelist))
            fromknownuniquenames = list(set(From_KnownNames))
            nameCountiterate=0
            for namez in highuniquenames:
                if " " in namez:
                    namesplit=namez.split(" ")
                    firstnamez=namesplit[0]
                    lastnamez=namesplit[1]
                sourceNumber = ("source"+str(nameCountiterate))
                thisArticlesSourcesDict["highAttributes"][namez] = {
                    "sourceNumber":sourceNumber,
                    "firstName":firstnamez,
                    "lastName":lastnamez
                    }
                nameCountiterate+=1

            nameCountiterate=0
            for namez in lowuniquenames:
                if " " in namez:
                    namesplit=namez.split(" ")
                    firstnamez=namesplit[0]
                    lastnamez=namesplit[1]
                sourceNumber = ("source"+str(nameCountiterate))
                thisArticlesSourcesDict["lowAttributes"][namez] = {
                    "sourceNumber":sourceNumber,
                    "firstName":firstnamez,
                    "lastName":lastnamez
                    }
                nameCountiterate+=1
                    
            nameCountiterate=0
            for namez in From_KnownNames:
                if " " in namez:
                    namesplit=namez.split(" ")
                    firstnamez=namesplit[0]
                    lastnamez=namesplit[1]
                sourceNumber = ("source"+str(nameCountiterate))
                thisArticlesSourcesDict["knownNames"][namez] = {
                    "sourceNumber":sourceNumber,
                    "firstName":firstnamez,
                    "lastName":lastnamez
                    }
                nameCountiterate+=1

            highuniquenames.clear()
            lowuniquenames.clear()
            fromknownuniquenames.clear()
            Highnamelist.clear()
            Lownamelist.clear()
            namelist.clear()
            From_KnownNames.clear()
            TEXT.clear()

            counter = counter +1
            current.sources = thisArticlesSourcesDict
            topStoriesDict[key] =current
            print(theArticleTitle, " is being added to the dictionary.")


        except Exception as e:
            blankvar=0
            #print()
            #print("There was an error with Story", theArticleTitle)
            #print()
            #print(e)

            From_KnownNames.clear()
            TEXT.clear()
            counter = counter +1
            topStoriesDict[key] =current
            
    else:
        blankvar=0
        #print(theArticleTitle, " is already in the dictionary.")

##########################################################################################################






##print()           
##print("Task is complete.")
##print()
##print()
##print()

################################## SaveData ###########################################################
##

saveQ=input("Do you want to save the changes?")
if saveQ.lower()[0]=="y":
    saveName=input("Please enter the .pickle filename you want: ")
    suffix=".pickle"
    filename=saveName+suffix
    with open(filename,'wb') as handle:
        pickle.dump(topStoriesDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    viewQ=input("Do you want to see the saved file? ")
    if viewQ.lower()[0]=="y":
        with open(filename,'rb') as handle:
            unserialized_data = pickle.load(handle)
        for i in range(0,10):
            print()
        print()
        print("Updated titles are: ")
        for key in unserialized_data:
            article=unserialized_data[key]
            print(key)
            print(key, " , ", article.section," , ", article.sources)
            #print()
else:
    nosaveQ=input("Do you want to see the changes that you are discarding?")
    if nosaveQ.lower()[0]=="y":
        for key in topStoriesDict:
            article=topStoriesDict[key]
            print(key, " , ", article.section, " , ", article.sources)



q1 = input ("Do you want to see the dictionary of known names?")
if q1.lower()[0] == "y":
    for i in range(0,3):
        print()
    print("The dictionary of known names is:  ",KnownNamesDict)
    
##
##    
##    
