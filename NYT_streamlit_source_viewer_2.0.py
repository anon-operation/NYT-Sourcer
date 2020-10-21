import streamlit as st
import pandas as pd
import numpy as np
import pickle
#import plotly.figure_factory as ff
import plotly.express as px
import plotly.io as pio
import datetime
pio.renderers.default = 'firefox'
import sqlite3


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



sqlfilename = "NYT.sqlite"

connex = sqlite3.connect(sqlfilename) #establish a connection
curs = connex.cursor() #CURS IS A CURSOR OBJECT CONTAINING OUR ENTIRE DB


def runQuery (fieldName,queryFieldName,queryValue):
    qString = "SELECT "+ fieldName + " FROM " + "ARTICLES"
    qString += " WHERE " + queryFieldName + " = ? ;"
    tup = (queryValue,)
    ans = curs.execute(qString,tup)
    if ans != "ERROR.":
        ansRows = ans.fetchall() #provides a list
    else:
        ansRows = []

    return ansRows

#@st.cache # Cache data after loading
def runPandaQuery (fieldName,queryFieldName,queryValue):
    qString = "SELECT "+ fieldName + " FROM " + "ARTICLES"
    qString += " WHERE " + queryFieldName + queryValue
    #tup = (queryValue,)
    #ansString=(qString,tup)
    df = pd.read_sql_query(qString, connex)
    #ans = curs.execute(qString,tup)
    connex.commit()
    #connex.close()
    return df





def highlight_name1(val):
    strung=str(val)
    loweredVal=strung.lower()
    loweredInput=name_user_input.lower()
    if loweredInput in loweredVal:
        color = 'red'
    else:
        color = 'black'
    return 'color: %s' % color


st.title("The Sourcer")



# create loading message
data_load_state=st.text('Loading data......')

# Load data
data=runPandaQuery ("*","Count"," ==1 ;")  ##(fieldName,queryFieldName,queryValue)  ("*","Section"," LIKE 'healt%';") 
df=pd.DataFrame(data)
df['Date']=pd.to_datetime(df['Date'], format='%Y-%m-%dT%H:%M:%S')
df['Publication Date']=df['Date']


data_load_state.text('')



########## Graphing
        
st.header("Find names that appear in news stories")

######### sidebar
st.sidebar.header("Welcome to the Sourcer App")
st.sidebar.subheader("This app shows names that appear in the text of New York Times Articles.")
moreInfo=st.sidebar.button("More info")
if moreInfo:
    st.sidebar.subheader("This app began as a question:")
    st.sidebar.subheader( "\"Is there a quick way to figure out who is mentioned in a New York Times story?\"")
    st.sidebar.subheader("From there the project grew...and is still growing!")
    st.sidebar.subheader("Each day the database of included articles grows. They come from the New York Times' front page.")
    st.sidebar.subheader("Additionally, I'm working to improve the accuracy of the name recognition, so that names like \"Mr. Trump\" and \"Donald Trump\" are seen as the same name and to exclude place names from recognition.")
    st.sidebar.subheader("The source code is availible for inspection at: https://github.com/anon-operation/NYT-Sourcer.git")

###############

modifyChart=st.checkbox("Click here for more oprtions")
if modifyChart:
    try:
        section_selectbox=st.selectbox("What section would you like to see?",
                                       ("All sections", "Health", "U.S.", "Business", "Upshot",
                                        "Magazine", "Briefing", "Podcasts",
                                        "Opinion", "N.Y. Region", "World",
                                        "Climate", "Dining", "Technology",
                                        "Style", "Sports", "Arts"))
        attribute_selectbox=st.selectbox("Type of attribute", ("All","NLTK", "High", "Low", "Known"))
        if attribute_selectbox == "All":
            attributeChoice='%'
        else:
            attributeChoice=attribute_selectbox.lower()
        startDate=st.date_input("Start date", pd.to_datetime("2020-09-29"))
        qDate1 = str((str(startDate))+"T00:00:00")
        endDate=st.date_input("End date", pd.to_datetime("2020-10-10"))
        qDate2 = str((str(endDate))+"T24:59:59")
        if startDate <= endDate:
            if section_selectbox=="All sections":
                fullQueryString = " BETWEEN "+"'"+qDate1+"'"+" AND "+"'"+qDate2+"'"+" AND Type LIKE  "+"'"+attributeChoice+"'"+" ;"
                data=runPandaQuery ("*","Date",fullQueryString)  ##(fieldName,queryFieldName,queryValue)  ("*","Section"," LIKE 'healt%';")
                df=pd.DataFrame(data)
                df['Date']=pd.to_datetime(df['Date'], format='%Y-%m-%dT%H:%M:%S')
                df['Publication Date']=df['Date']
                df3=df
                fig=px.bar(df3, x="Name", y="Count", color="Section",
                hover_data=["Title", "Url", "Publication Date"])
                st.plotly_chart(fig, use_container_width=True)
            else:
                try:
                    lowercaseSelection=section_selectbox.lower()
                    if lowercaseSelection=="u.s.":
                        lowercaseSelection="us"
                    elif lowercaseSelection=="n.y. region":
                        lowercaseSelection="nyregion"
                    fullQueryString = " BETWEEN "+"'"+qDate1+"'"+" AND "+"'"+qDate2+"'"+" AND Type LIKE  "+"'"+attributeChoice+"'"+" AND Section LIKE "+"'"+lowercaseSelection+"'"+" ;"
                    data=runPandaQuery ("*","Date",fullQueryString)  ##(fieldName,queryFieldName,queryValue)  ("*","Section"," LIKE 'healt%';")
                    df=pd.DataFrame(data)
                    df['Date']=pd.to_datetime(df['Date'], format='%Y-%m-%dT%H:%M:%S')
                    df['Publication Date']=df['Date']
                    df3=df
                    fig=px.bar(df3, x="Name", y="Count", color="Section",
                    hover_data=["Title", "Url", "Publication Date", "Name"])
                    st.plotly_chart(fig, use_container_width=True)
                except:
                    st.error("Error: The database has no stories for the given dates and section. Try a wider date range or click All sections")
        else:
            st.error("Error: The end date must be after the start date.")
    except:
        st.error("Error: The database has no stories for the given dates and section. Try a wider date range or click All sections")
else:

    st.text("Chart shows names that appear more than once.")
    df3=df.loc[df.duplicated(subset='Name', keep=False), :]
    fig=px.bar(df3, x="Name", y="Count", color="Section",
            hover_data=["Title", "Url", "Publication Date"])
    st.plotly_chart(fig, use_container_width=True)



############################### Tabling

showData=st.checkbox("Show the raw data")

if(showData==True):
    if modifyChart:
######## Sort data based on user's search term
        matchGraph=st.checkbox("Show data displayed in selected section")
        if matchGraph:
            if (section_selectbox =="All sections"):
                st.subheader('Raw Data from '+section_selectbox+' of New York Times')
            else:
                st.subheader('Raw Data from the '+section_selectbox+' section of New York Times')
            name_user_input = st.text_input("Search for a name.", "")
            lowerName=name_user_input.lower()
            indexList=df3[df3['Name'].str.contains(lowerName)]
            restOf=df3[~df3['Name'].str.contains(lowerName)]
            sortedDf=pd.concat([indexList, restOf], ignore_index=True, sort=False)
            st.dataframe(sortedDf.style.applymap(highlight_name1))
        else:
            st.subheader('Raw Data from entire database')
            name_user_input = st.text_input("Search for a name.", "")
            lowerName=name_user_input.lower()
            indexList=df[df['Name'].str.contains(lowerName)]
            restOf=df[~df['Name'].str.contains(lowerName)]
            sortedDf=pd.concat([indexList, restOf], ignore_index=True, sort=False)
            st.dataframe(sortedDf.style.applymap(highlight_name1))
    else:
        st.subheader('Raw Data from entire database')
        name_user_input = st.text_input("Search for a name.", "")
        lowerName=name_user_input.lower()
        indexList=df[df['Name'].str.contains(lowerName)]
        restOf=df[~df['Name'].str.contains(lowerName)]
        sortedDf=pd.concat([indexList, restOf], ignore_index=True, sort=False)
        st.dataframe(sortedDf.style.applymap(highlight_name1))


################ Search by Article
st.text("")
st.subheader("Search for a specific article")
article_user_input = st.text_input("Search for an article.", "")
lowerArtName=article_user_input.lower()

data=runPandaQuery ("*","Count"," ==1 ;")  ##(fieldName,queryFieldName,queryValue)  ("*","Section"," LIKE 'healt%';") 
articleDf=pd.DataFrame(data)
articleDf['Date']=pd.to_datetime(articleDf['Date'], format='%Y-%m-%dT%H:%M:%S')
articleDf['Publication Date']=articleDf['Date']
articleDf['Title']=articleDf['Title'].str.lower()
articleDf.loc[:,'Title']=articleDf.loc[:,'Title'].str.replace("`|’", "'", regex=True)
artIndexList=articleDf[articleDf['Title'].str.contains(lowerArtName)]
if artIndexList.empty:
    st.error("There are no article titles that contain "+article_user_input)
else:
    st.dataframe(artIndexList)
    printList=st.button("Get list of names in aticle(s) with \""+article_user_input+"\" in the title")
    if printList:
        listDf=artIndexList['Name']
        st.text("You can highlight and copy this list of names:")
        for name in listDf:
            st.text(name)

 


