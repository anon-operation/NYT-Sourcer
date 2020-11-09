##method 1 from: https://stackoverflow.com/questions/20290870/improving-the-extraction-of-human-names-with-nltk/24119115
## Method 2Code from https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
## https://github.com/susanli2016
## Git test



################### pREREQS ##############################
import requests
import json
import pickle
import http.cookiejar
import re
import urllib
from bs4 import BeautifulSoup
### you might need to pip install html5lib
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
from nameparser.parser import HumanName
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm ###This is the recognition model...it can be substituted.
import en_core_web_lg
nlp = en_core_web_lg.load()






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

def urlToString(url):
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html5lib')
    for script in soup(["script", "style", 'aside']):
        script.extract()
    return ' ' .join(re.split(r'[\n\t]+', soup.get_text()))


attributions = ["said","says","according","explains","explained","agreed"]
High_attributions = ["said","says","according","explains","explained", "explain","say"]
Low_attributions = ["recalls","recalled","thinks","think","describe","agreed","agrees","describes","described","points""pointed","point","indicates","indicate","indicated"]

Highnamelist = []
Lownamelist = []
namelist = []
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

def NERmethod(text):
    nlp = en_core_web_sm.load()
    doc=nlp(text)
    nerNameList=[]
    for x in doc.ents:
        if x.label_ == "PERSON":
            if x.text not in nerNameList:
                nerNameList.append(x.text)
    #print(nerNameList)
    return nerNameList

def SaidFinder(text):
    #noPunc = text.translate(str.maketrans('', '', string.punctuation))
    NumSourceDict = {}
    noPunc = re.sub(r'[^\w\s]','',text)
    noPuncNames = []
    for name in nerNameList:
        cleanName = re.sub(r'[^\w\s]','',name)
        noPuncNames.append(cleanName)
    #print(noPuncNames)
    words = noPunc.split(" ")
    wordCounter=(-1)
    for i in words:
        wor = i
        wordCounter+=1
        #print(wor)
        if wor in High_attributions:
            index = words.index(wor)
            #print("Index of said is: ", wordCounter)
            #print("It's: ", words[index])
            notFound = True
            lookupNum = 1
            while notFound:
                try:
                    toExamineForward = words[wordCounter+lookupNum]
                    toExamineBackward = words[wordCounter-lookupNum]
                except:
                    #print("error")
                    notFound = False
                #print("Looking at:",toExamineForward,toExamineBackward)
                hasFound = False
                for nameS in noPuncNames:
                    #print(nameS)
                    if hasFound == False:
                        if ((toExamineBackward in nameS) or (toExamineForward in nameS)):
                            #print("Source is: ", nameS)
                            NumSourceDict[wordCounter] = nameS
                            hasFound = True
                            notFound = False
##                        else:
##                            if hasFound == False:
##                                if toExamineBackward in nameS:
##                                    print("Source is: ", nameS)
##                                    hasFound = True
##                                    notFound = False
                lookupNum+=1
        notFound = True
    return NumSourceDict

def QuoteFinder(text):
    quoteList=[]
    words = text.split(" ")
    startVar = 0
    wordNum = (0)
    wNum = (-1)
    endQuoteList = []
    for word in words:
        #wNum+=1
        breakDown = list(word)
        #print(breakDown)
##        if ("”" in breakDown or "“" in breakDown or "\"" in breakDown):
        if ("“" in breakDown or "\"" in breakDown):
            if wordNum not in endQuoteList: 
                print(word)
                if startVar==0:
                    notFound = True
                    nextNum = wordNum
                    while notFound:
                        try:
                            nextWord = words[nextNum+1]
                            nextNextWord = words[nextNum+2]
##                            print(nextWord,nextNextWord)
##                            print(nextNum)
                            if ("”" in nextWord or "“" in nextWord or "\"" in nextWord):
                                print("Quote ends with ", nextWord)
                                print("This is word number: ", nextNum)
                                endQuoteList.append(nextNum)
                                notFound = False
                                startVar = 0
                            else:
                                nextNum+=1
                        except:
                            notFound = False
##            if startVar==1:
##                wNum+=1
        wordNum+=1
    return endQuoteList
                
def NumericalCompare(dictionary,aList):
    likelySources = []
    theList = dictionary.keys()
    for item in aList:
        likelySourceNumber = min(theList, key=lambda x:abs(x-item))
        source = dictionary[likelySourceNumber]
        likelySources.append(source)
    return likelySources


##################### Incorporate previous data  ########################
automateQ = input("Do you want to automate the process? ")
if automateQ.lower()[0]=="y":
    automate  = "ON"
else:
    automate = "OFF"



##prefixFile="septHistorical"  #input("Please type the name of the .pickle file you'd like to add to. You don't need to type the .pickle part. ")
##suffix=".pickle"
##selectedFileToAddTo=(prefixFile+suffix)
##
##try:
##    with open(KnownNamesLister,'rb') as handle:
##        unserialized_data_Known = pickle.load(handle)
##    RunningKnownNamesDict=Unserialized_data_Known
##except:
##    RunningKnownNamesDict=[]
##    print("There is a blank list of known names....If this is an error, check for the picklefile.")
##
##
##with open(selectedFileToAddTo,'rb') as handle:
##    unserialized_data = pickle.load(handle)
##    
##q0 =input("Do you want to see the previously saved dictionary of sources?  ")
##if q0.lower()[0]=="y":
##    print("The packed and unpacked data is:")
##    print()
##    for key in unserialized_data:
##        article=unserialized_data[key]
##        print(key, " , ", article.section," , ", article.sources)
##        print()
##
##
##q0_1 =input("Do you want to add to the previously saved dictionary of sources?  ")
##if q0.lower()[0]=="y":
##    topStoriesDict = unserialized_data
##    checkList=[]
##    for key in topStoriesDict:
##        checkList.append(key)
##    print("The known titles are: ")
##    print(checkList)
##else:
##    topStoriesDict = {} ##{headlin:StoryMetadata object}
##    checkList=[]

topStoriesDict = {} ##{headlin:StoryMetadata object}
checkList=[]
RunningKnownNamesDict=[]
commonErrorsList=["sectionssearchskip","salesite mapcanadainternationalhelpsubscriptions","paperpage",
                  "choicesprivacy","information navigation","getty","vote tracking","facebook twitter",
                  "twitter", "studio your ad", "york times","new year","the new york times","the new",
                  "ad choices privacy","the new york timesthe","bycontinue","supported continue",
                  "index site information","brand studio your","advertisementcontinue","sections skip",
                  "getty images by","easttoday"]
SuccessRatioDict = {"BS":{"success":[],
                          "failure":[]},
                    "HTML":{"success":[],
                            "failure":[]}
                    }

HTMLsuccessList=[]
HTMLfailureList=[]
BSsuccessList=[]
BSfailureList=[]

#print("topStoriesDict is: ", topStoriesDict)
###########################################################################################################
##KnownNames = RunningKnownNamesDict

##yearQ=input("What year do you want? ")
##monthQ=input("What month? ")
##preReq="https://api.nytimes.com/svc/archive/v1/"+str(yearQ)+"/"+str(monthQ)+".json?api-key="

yearS="2020"
##monthS=["4","5","6","7","8","9"]
monthS=["9"]

for month in monthS:
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
    print("Month:",month)
    preReq="https://api.nytimes.com/svc/archive/v1/"+str(yearS)+"/"+str(month)+".json?api-key="

    your_key = ""
    getReq=(preReq+your_key)
    result = requests.get(getReq)
    print(result.status_code) #200 is all good
    dictMain = json.loads(result.text)
##    for key in dictMain['response']['docs']:
    lll=[1]
    for num in lll:
        key = dictMain['response']['docs'][num]
        try:
            url=key['web_url']
            title=key['headline']['main']
            date=key['pub_date']
            author=key['byline']['original']
            section=key['section_name']
            authorsplit=author.split(",")
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
                print(title, " is a new addition to the dictionary.")
                new=StoryMetadata()
                new.pubDate=date
                new.section=section
                new.url=url
                new.author=authorsplit
                topStoriesDict[title]=new
        except:
            ran=0


    ##########################################MAIN BODY###################

    counter=0
    TEXT = []
    TEXT.clear()
    ALLFULLTEXTS = []
    for key in topStoriesDict:
        current=topStoriesDict[key]
        if key not in checkList:
            theArticleTitle=key
            url=current.url
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
    ##            thisArticlesSourcesDict={"NLTK":[],
    ##                                     "highAttributes_HEM":[],
    ##                                     "lowAttributes":[],
    ##                                     "knownNames":[],
    ##                                     "NER":[]}


    ####################################################################
                #print("Good at checkpoint 1")

    ###############################################################################
                
                thisArticlesSourcesDict={"HTML_1":{"NLTK":[],
                                         "high":[],
                                         "low":[],
                                         "known":[],
                                         "NER":[],
                                         "Quotations":[]},
                                         "HTML_BS":{"NLTK":[],
                                         "high":[],
                                         "low":[],
                                         "known":[],
                                         "NER":[],
                                         "Quotations":[]}
                                         }

                new=Article()
                try:

        ####################################### HTML PARSE 1 ##########################################

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
                    #print("Something Happened...is Good at checkpoint 2")
                    text = fulltext
        ####################################### NLTK ##########################################
                    names = get_human_names(text)
                    nameListNLTK = []
                    for name in names:
                        if name not in current.author:
                            nameListNLTK.append(name)

                    thisArticlesSourcesDict["HTML_1"]["NLTK"] = nameListNLTK
                    #print("NLTKS are: ", nameListNLTK)
                    current.sources = thisArticlesSourcesDict
                except Exception as e:
                    print(e)
                    print("Error is in HTML 1 NLTK")

    ####################################### NER ##########################################
                doc=nlp(text)
                nerNameList=[]
                nerOrgList=[]
                for x in doc.ents:
                    if x.label_ == "PERSON":
                        if x.text not in nerNameList:
                            if x.text not in current.author:
                                nerNameList.append(x.text)
                    if x.label_ == "ORG":
                        if x.text not in nerOrgList:
                            if x.text not in current.author:
                                nerOrgList.append(x.text)
                thisArticlesSourcesDict["HTML_1"]["NER"] = nerNameList
                thisArticlesSourcesDict["HTML_1"]["NER_ORGS"] = nerOrgList

                try:
                    for name in thisArticlesSourcesDict["HTML_1"]["NER"]:
                        if name.lower() in commonErrorsList:
                            thisArticlesSourcesDict["HTML_1"]["NER"].remove(name) 
                    current.sources = thisArticlesSourcesDict
                except Exception as e:
                    print(e)
                    print("Error is in common error removal HTML_1 NER")
                try:
                    for name in thisArticlesSourcesDict["HTML_1"]["NER_ORGS"]:
                        if name.lower() in commonErrorsList:
                            thisArticlesSourcesDict["HTML_1"]["NER_ORGS"].remove(name) 
                    current.sources = thisArticlesSourcesDict
                except Exception as e:
                    print(e)
                    print("Error is in common error removal HTML_1 NER_ORGS")

                current.sources = thisArticlesSourcesDict
                print(nerNameList)
                try:
                    for name in thisArticlesSourcesDict["HTML_1"]["NER"]:
                        alphabetize(name)
                except Exception as e:
                    print(e)
                    print("HTML 1 NER alphabetize failed")


    ####################################### Remove Mr. & Alphabetize ##########################################
                try:
                    deMrList=[]
                    for name in thisArticlesSourcesDict["HTML_1"]["NLTK"]:
                        if "Mr." in name:
                            non = name.replace("Mr. ", "")
                            deMrList.append(non)
                        if "Mr." not in name:
                            deMrList.append(name)
                    thisArticlesSourcesDict["HTML_1"]["NLTK"]=deMrList
                    current.sources = thisArticlesSourcesDict

                except Exception as e:
                    print(e)
                    print("Error is in MR.part 1")

                try:
                    deMrsList=[]
                    for name in thisArticlesSourcesDict["HTML_1"]["NLTK"]:
                        if "Mrs." in name:
                            non = name.replace("Mrs. ", "")
                            deMrsList.append(non)
                        if "Mrs." not in name:
                            deMrsList.append(name)
                    thisArticlesSourcesDict["HTML_1"]["NLTK"]=deMrsList
                    current.sources = thisArticlesSourcesDict

                except Exception as e:
                    print(e)
                    print("Error is in MRs.part 1")

                try:
                    deMsList=[]
                    for name in thisArticlesSourcesDict["HTML_1"]["NLTK"]:
                        if "Ms." in name:
                            non = name.replace("Ms. ", "")
                            deMsList.append(non)
                        if "Ms." not in name:
                            deMsList.append(name)
                    thisArticlesSourcesDict["HTML_1"]["NLTK"]=deMsList
                    current.sources = thisArticlesSourcesDict

                except Exception as e:
                    print(e)
                    print("Error is in MRs.part 1")

                try:
                    for name in thisArticlesSourcesDict["HTML_1"]["NLTK"]:
                        if name.lower() in commonErrorsList:
                            thisArticlesSourcesDict["HTML_1"]["NLTK"].remove(name) 
                    current.sources = thisArticlesSourcesDict

                except Exception as e:
                    print(e)
                    print("Error is in common error removalpart 1")



                    
                try:
                    for name in thisArticlesSourcesDict["HTML_1"]["NLTK"]:
                        alphabetize(name)
                except Exception as e:
                    print(e)
                    print("HTML 1 NLTK alphabetize failed")

    ####################################### Attribute Methods ##########################################

                try:
                    words = text.split()
                      
                    for i in words:
                        nearby = find_prev_next(i, words)
                        for x in High_attributions:
                            if x in nearby:
                                joined = ' '.join(nearby)
                                if ((len(re.findall('([A-Z][a-z]+)', joined)))>1):
                                    t = re.findall('([A-Z][a-z]+)', joined)
                                    name = ' '.join(t)
                                    if name not in current.author:
                                        Highnamelist.append(name)
                except:
                    blank=[]
                try:
                    words = text.split()
                    for i in words:
                        nearby = find_prev_next(i, words)
                        for x in Low_attributions:
                            if x in nearby:
                                joined = ' '.join(nearby)
                                if ((len(re.findall('([A-Z][a-z]+)', joined)))>1):
                                    t = re.findall('([A-Z][a-z]+)', joined)
                                    name = ' '.join(t)
                                    if name not in current.author:
                                        Lownamelist.append(name)
                except:
                    blank=[]


                try:
                    words = text.split()
                    for i in words:
                        try:
                            nearby = find_next(i, words)
                        except:
                            blank=[]
                        for x in nearby:
                            try:
                                letter = x.lower()[0]
                                namelisting = KnownNamesDict[letter]
                                if x in namelisting:
                                    joined = ' '.join(nearby)
                                    if ((len(re.findall('([A-Z][a-z]+)', joined)))>1):
                                        t = re.findall('([A-Z][a-z]+)', joined)
                                        name = ' '.join(t)
                                        if name not in current.author:
                                            From_KnownNames.append(name)

                            except:
                                blank=[]
                except Exception as e:
                    print(e)
                    print("Error in HTML 1 known name process")
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
                thisArticlesSourcesDict["HTML_1"]["high"] = list(highuniquenames)
                thisArticlesSourcesDict["HTML_1"]["low"] = list(lowuniquenames)
                thisArticlesSourcesDict["HTML_1"]["known"] = list(fromknownuniquenames) ############################### IT;s here

                try:
                    for name in thisArticlesSourcesDict["HTML_1"]["high"]:
                        if name.lower() in commonErrorsList:
                            thisArticlesSourcesDict["HTML_1"]["high"].remove(name) 
                    current.sources = thisArticlesSourcesDict
                except Exception as e:
                    print(e)
                    print("Error is in common error removal HTML_1 high")
                try:
                    for name in thisArticlesSourcesDict["HTML_1"]["low"]:
                        if name.lower() in commonErrorsList:
                            thisArticlesSourcesDict["HTML_1"]["low"].remove(name) 
                    current.sources = thisArticlesSourcesDict
                except Exception as e:
                    print(e)
                    print("Error is in common error removal HTML_1 low")

                current.sources = thisArticlesSourcesDict
                topStoriesDict[key] = current
                
    ####################################### Quotation Methods ##########################################
                nerNameList=NERmethod(text)
                NumSourceDict = SaidFinder(text)
                qList=QuoteFinder(text)
                theMathematicalSources = NumericalCompare(NumSourceDict,qList)
                quoteSources = list(set(theMathematicalSources))
                lowQuoteSources=[]
                for name in quoteSources:
                    lowered = name.lower()
                    lowQuoteSources.append(lowered)
                thisArticlesSourcesDict["HTML_1"]["Quotations"] = list(lowQuoteSources)
                current.sources = thisArticlesSourcesDict
                topStoriesDict[key] = current
                

                    
                print("*****************************************************") 
                print("End HTML Quote List: ", qList)
                print("All Names: ", nerNameList)
                print(theMathematicalSources)


    ####################################### Clear Variables ##########################################


                highuniquenames.clear()
                lowuniquenames.clear()
                fromknownuniquenames.clear()
                Highnamelist.clear()
                Lownamelist.clear()
                namelist.clear()
                From_KnownNames.clear()
                TEXT.clear()

                counter = counter +1
                #print(theArticleTitle, " is being added to the dictionary via HTML 1.")
                HTMLsuccessList.append(theArticleTitle)
                #print("HTML Success: ", HTMLsuccessList)
                SuccessRatioDict["HTML"]["success"] = HTMLsuccessList
                SuccessRatioDict["HTML"]["failure"] = HTMLfailureList
                SuccessRatioDict["BS"]["success"] = BSsuccessList
                SuccessRatioDict["BS"]["failure"] = BSfailureList
    ##            for key in topStoriesDict:
    ##                article=topStoriesDict[key]
    ##                print(key, " , ", article.section, " , ", article.sources)
                #for i in range(0,5):
                   # print()

            except Exception as e:
                blankvar=0
                #print()
                print("There was an error with Story", theArticleTitle)
                HTMLfailureList.append(theArticleTitle)
                print(url)
                #print()
                print(e)
                SuccessRatioDict["HTML"]["success"] = HTMLsuccessList
                SuccessRatioDict["HTML"]["failure"] = HTMLfailureList
                SuccessRatioDict["BS"]["success"] = BSsuccessList
                SuccessRatioDict["BS"]["failure"] = BSfailureList
                From_KnownNames.clear()
                TEXT.clear()
                counter = counter +1
                topStoriesDict[key] = current
            try:
    ####################################### Beautiful Soup ######################################################
                theStorySoFar = urlToString(url)
     ####################################### NLTK ##########################################
                names = get_human_names(theStorySoFar)
                nameListNLTK = []
                for name in names:
                    firname = str(HumanName(name).first)
                    laname = str(HumanName(name).last)
                    try:
                        alphabetize(firname)
                        alphabetize(laname)
                    except Exception as e:
                        blankvar=0
                        #print()
                        #print("Either the first or last name is missing, so alphabetize failed. No big deal")
                    if name not in current.author:
                        nameListNLTK.append(name)

                thisArticlesSourcesDict["HTML_BS"]["NLTK"] = nameListNLTK
                #print("NLTKS are: ", nameListNLTK)
                current.sources = thisArticlesSourcesDict


    ####################################### NER ##########################################
                doc=nlp(theStorySoFar)
                nerNameList=[]
                nerOrgList=[]
                for x in doc.ents:
                    if x.label_ == "PERSON":
                        if x.text not in nerNameList:
                            if x.text not in current.author:
                                nerNameList.append(x.text)
                    if x.label_ == "ORG":
                        if x.text not in nerOrgList:
                            if x.text not in current.author:
                                nerOrgList.append(x.text)
                thisArticlesSourcesDict["HTML_BS"]["NER"] = nerNameList
                thisArticlesSourcesDict["HTML_BS"]["NER_ORGS"] = nerOrgList

                try:
                    for name in thisArticlesSourcesDict["HTML_BS"]["NER"]:
                        if name.lower() in commonErrorsList:
                            thisArticlesSourcesDict["HTML_BS"]["NER"].remove(name)
                            print("Common error name removed: ", name)

                    current.sources = thisArticlesSourcesDict
                except Exception as e:
                    print(e)
                    print("Error is in common error removal BS NER")
                try:
                    for name in thisArticlesSourcesDict["HTML_BS"]["NER_ORGS"]:
                        if name.lower() in commonErrorsList:
                            thisArticlesSourcesDict["HTML_BS"]["NER_ORGS"].remove(name)
                            print("Common error name removed: ", name)
                    current.sources = thisArticlesSourcesDict
                except Exception as e:
                    print(e)
                    print("Error is in common error removal BS NER Org")

                current.sources = thisArticlesSourcesDict
                try:
                    for name in thisArticlesSourcesDict["HTML_BS"]["NER"]:
                        alphabetize(name)
                except Exception as e:
                    print(e)
                    print("BS NER alphabetize failed")


    ####################################### Remove Mr. ##########################################

                try:
                    deMrList=[]
                    for name in thisArticlesSourcesDict["HTML_BS"]["NLTK"]:
                        if "Mr." in name:
                            non = name.replace("Mr. ", "")
                            deMrList.append(non)
                        if "Mr." not in name:
                            deMrList.append(name)
                    thisArticlesSourcesDict["HTML_BS"]["NLTK"]=deMrList
                    current.sources = thisArticlesSourcesDict

                except Exception as e:
                    print(e)
                    print("Error is in MR.part 1")

                try:
                    deMrsList=[]
                    for name in thisArticlesSourcesDict["HTML_BS"]["NLTK"]:
                        if "Mrs." in name:
                            non = name.replace("Mrs. ", "")
                            deMrsList.append(non)
                        if "Mrs." not in name:
                            deMrsList.append(name)
                    thisArticlesSourcesDict["HTML_BS"]["NLTK"]=deMrsList
                    current.sources = thisArticlesSourcesDict

                except Exception as e:
                    print(e)
                    print("Error is in MRs.part 1")

                try:
                    deMsList=[]
                    for name in thisArticlesSourcesDict["HTML_BS"]["NLTK"]:
                        if "Ms." in name:
                            non = name.replace("Ms. ", "")
                            deMsList.append(non)
                        if "Ms." not in name:
                            deMsList.append(name)
                    thisArticlesSourcesDict["HTML_BS"]["NLTK"]=deMsList
                    current.sources = thisArticlesSourcesDict

                except Exception as e:
                    print(e)
                    print("Error is in MRs.part 1")

                try:
                    for name in thisArticlesSourcesDict["HTML_BS"]["NLTK"]:
                        if name.lower() in commonErrorsList:
                            thisArticlesSourcesDict["HTML_BS"]["NLTK"].remove(name) 
                    current.sources = thisArticlesSourcesDict

                except Exception as e:
                    print(e)
                    print("Error is in common error removal BS")


                    
                try:
                    for name in thisArticlesSourcesDict["HTML_BS"]["NLTK"]:
                        alphabetize(name)
                except Exception as e:
                    print(e)
                    print("BS NLTK alphabetize failed")


    ####################################### Attribute Methods ##########################################
                Highnamelist = []
                Lownamelist = []
                From_KnownNames = []
                
                try:
                    words = theStorySoFar.split()
                    for i in words:
                        nearby = find_prev_next(i, words)
                        for x in High_attributions:
                            if x in nearby:
                                joined = ' '.join(nearby)
                                if ((len(re.findall('([A-Z][a-z]+)', joined)))>1):
                                    t = re.findall('([A-Z][a-z]+)', joined)
                                    name = ' '.join(t)
                                    if name not in current.author:
                                        Highnamelist.append(name)
                except:
                    blank=[]
                try:
                    words = theStorySoFar.split()
                    for i in words:
                        nearby = find_prev_next(i, words)
                        for x in Low_attributions:
                            if x in nearby:
                                joined = ' '.join(nearby)
                                if ((len(re.findall('([A-Z][a-z]+)', joined)))>1):
                                    t = re.findall('([A-Z][a-z]+)', joined)
                                    name = ' '.join(t)
                                    if name not in current.author:
                                        Lownamelist.append(name)
                except:
                    blank=[]
                    

                try:
                    words = theStorySoFar.split()
                    for i in words:
                        try:
                            nearby = find_next(i, words)
                        except:
                            blank=[]
                        for x in nearby:
                            try:
                                letter = x.lower()[0]
                                namelisting = KnownNamesDict[letter]
                                if x in namelisting:
                                    joined = ' '.join(nearby)
                                    if ((len(re.findall('([A-Z][a-z]+)', joined)))>1):
                                        t = re.findall('([A-Z][a-z]+)', joined)
                                        name = ' '.join(t)
                                        if name not in current.author:
                                            From_KnownNames.append(name)

                            except:
                                blank=[]
                except Exception as e:
                    print(e)
                    print("Error in HTML 1 known name process")
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
                thisArticlesSourcesDict["HTML_BS"]["high"] = list(highuniquenames)
                thisArticlesSourcesDict["HTML_BS"]["low"] = list(lowuniquenames)
                thisArticlesSourcesDict["HTML_BS"]["known"] = list(fromknownuniquenames)
                try:
                    for name in thisArticlesSourcesDict["HTML_BS"]["high"]:
                        if name.lower() in commonErrorsList:
                            thisArticlesSourcesDict["HTML_BS"]["high"].remove(name) 
                    current.sources = thisArticlesSourcesDict
                except Exception as e:
                    print(e)
                    print("Error is in common error removal BS high")
                try:
                    for name in thisArticlesSourcesDict["HTML_BS"]["low"]:
                        if name.lower() in commonErrorsList:
                            thisArticlesSourcesDict["HTML_BS"]["low"].remove(name) 
                    current.sources = thisArticlesSourcesDict
                except Exception as e:
                    print(e)
                    print("Error is in common error removal BS high")

                current.sources = thisArticlesSourcesDict
                topStoriesDict[key] = current
                
    ####################################### Quotation Methods ##########################################
                nerNameList=NERmethod(theStorySoFar)
                NumSourceDict = SaidFinder(theStorySoFar)
                qList=QuoteFinder(theStorySoFar)
                theMathematicalSources = NumericalCompare(NumSourceDict,qList)
                quoteSources = list(set(theMathematicalSources))
                lowQuoteSources=[]
                for name in quoteSources:
                    lowered = name.lower()
                    lowQuoteSources.append(lowered)
                thisArticlesSourcesDict["HTML_BS"]["Quotations"] = list(lowQuoteSources)
                current.sources = thisArticlesSourcesDict
                topStoriesDict[key] = current
                

    ####################################### Clear Variables ##########################################


                highuniquenames.clear()
                lowuniquenames.clear()
                fromknownuniquenames.clear()
                Highnamelist.clear()
                Lownamelist.clear()
                namelist.clear()
                From_KnownNames.clear()
                TEXT.clear()


                counter = counter +1
                #print(theArticleTitle, " is being added to the dictionary via HTML BS.")
                
                BSsuccessList.append(theArticleTitle)
                #print("BS Success: ", BSsuccessList)
                SuccessRatioDict["HTML"]["success"] = HTMLsuccessList
                SuccessRatioDict["HTML"]["failure"] = HTMLfailureList
                SuccessRatioDict["BS"]["success"] = BSsuccessList
                SuccessRatioDict["BS"]["failure"] = BSfailureList
                
                for i in range(0,5):
                    print()          
            except Exception as e:
                print(e)
                print("Error in beautiful soup parse")
                BSfailureList.append(theArticleTitle)
                From_KnownNames.clear()
                TEXT.clear()
                counter = counter +1
                topStoriesDict[key] = current
                SuccessRatioDict["HTML"]["success"] = HTMLsuccessList
                SuccessRatioDict["HTML"]["failure"] = HTMLfailureList
                SuccessRatioDict["BS"]["success"] = BSsuccessList
                SuccessRatioDict["BS"]["failure"] = BSfailureList
     
        else:
            blankvar=0
            #print(theArticleTitle, " is already in the dictionary.")
    ##    print()
    ##    print("#################################################################")
    ##    print(theArticleTitle)
    ##    print(current.sources)
    ##    print(current.author)
    ##    print()
        for key in KnownNamesDict:
            listOfNames=KnownNamesDict[key]
            cleaned = list(set(listOfNames))
            KnownNamesDict[key] = list(cleaned)
        #print(KnownNamesDict)
            #print(theArticleTitle)
        #print(SuccessRatioDict)

    ##########################################################################################################
    SuccessRatioDict["HTML"]["success"] = HTMLsuccessList
    SuccessRatioDict["HTML"]["failure"] = HTMLfailureList
    SuccessRatioDict["BS"]["success"] = BSsuccessList
    SuccessRatioDict["BS"]["failure"] = BSfailureList



################################## SaveData ###########################################################
##

print(topStoriesDict)
    
if automate == "ON":
    saveQ="y"
else:
    saveQ=input("Do you want to save the changes?")
if saveQ.lower()[0]=="y":
    if automate  == "ON":
        saveName="theHistoricalData"
    else: 
        saveName=input("Please enter the .pickle filename you want: ")
    suffix=".pickle"
    filename=saveName+suffix
    with open(filename,'wb') as handle:
        pickle.dump(topStoriesDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    if automate  == "ON":
        viewQ="y"
    else:
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


if automate  == "ON":
    q1 = "y"
else:
    q1 = input ("Do you want to see the dictionary of known names?")
if q1.lower()[0] == "y":
    for i in range(0,3):
        print()
    print("The dictionary of known names is:  ",KnownNamesDict)

saveQ3="y"
if saveQ3.lower()[0]=="y":
    if automate  == "ON":
        saveName="KnownNamesData"
    else:
        saveName=input("Please enter the .pickle filename you want: ")
    suffix=".pickle"
    filename=saveName+suffix
    with open(filename,'wb') as handle:
        pickle.dump(KnownNamesDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    if automate  == "ON":
        viewQ="y"
    else:
        viewQ=input("Do you want to see the saved file? ")
    if viewQ.lower()[0]=="y":
        with open(filename,'rb') as handle:
            unserialized_data = pickle.load(handle)
        for i in range(0,10):
            print()
        print()
        print("Known Names are: ")
        print(unserialized_data)


saveQ4="y"
if saveQ4.lower()[0]=="y":
    if automate  == "ON":
        saveName="ParseSuccessRatioData"
    else:
        saveName=input("Please enter the .pickle filename you want for the success rate data: ")
    suffix=".pickle"
    filename=saveName+suffix
    with open(filename,'wb') as handle:
        pickle.dump(SuccessRatioDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    if automate  == "ON":
        viewQ="y"
    else:
        viewQ=input("Do you want to see the saved file? ")
    if viewQ.lower()[0]=="y":
        with open(filename,'rb') as handle:
            unserialized_data = pickle.load(handle)
        for i in range(0,10):
            print()
        print()
        print("Success/failure data is: ")
        print(unserialized_data)


 
