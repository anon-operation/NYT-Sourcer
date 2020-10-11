import streamlit as st
import pandas as pd
import numpy as np
import pickle
#import plotly.figure_factory as ff
import plotly.express as px
import plotly.io as pio
import datetime
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



st.title("The Sourcer")

filename="runningDatabase"
totalFileName=(filename+".pickle")
outfile = open("streamlitData.csv", "w", encoding='utf-8')

@st.cache # Cache data after loading
def load_NYT_data():
    with open(totalFileName,'rb') as handle:
        unserialized_data = pickle.load(handle)
    nameTallylist = []
    print("Name", "Section", "Url", "Date", "Title", "Count",sep =",",file=outfile)
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
            for name in NLTKs:
                lower=name.lower()
                print(lower, section, url, fixedDate, title, count, sep=",",file=outfile)
        except:
            tryVar=0
    outfile.flush()
    outfile.close()

    df=pd.read_csv('streamlitData.csv', sep=',')

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





# create loading message
data_load_state=st.text('Loading data......')

# Load data
data=load_NYT_data()
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
        startDate=st.date_input("Start date", pd.to_datetime("2020-09-29"))
        theStart=pd.to_datetime(str(startDate))
        endDate=st.date_input("End date", pd.to_datetime("2020-10-10"))
        theEnd=pd.to_datetime(str(endDate))
        if startDate < endDate:
            df['Date'] = pd.to_datetime(df['Date'])
            dfDated=df.set_index(['Date'])
            df3=dfDated.loc[str(theStart):str(theEnd)]
            if section_selectbox=="All sections":
                fig=px.bar(df3, x="Name", y="Count", color="Section",
                    hover_data=["Title", "Url", "Publication Date"])
                st.plotly_chart(fig, use_container_width=True)
            else:
                try:
                    lowercaseSelection=section_selectbox.lower()
                    if lowercaseSelection=="u.s.":
                        df3=df3[df3['Section'].str.contains("us")]
                        df3=df3[~df3['Section'].str.contains("ness")]
                        fig=px.bar(df3, x="Name", y="Count", color="Section",
                            hover_data=["Title", "Url", "Publication Date"])
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        df3=df3[df3['Section'].str.contains(lowercaseSelection)]
                        fig=px.bar(df3, x="Name", y="Count", color="Section",
                                hover_data=["Title", "Url", "Publication Date"])
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


##
##DATE_COLUMN='date/time'
##DATA_URL=('https://s3-us-west-2.amazonaws.com/'
##          'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
##
##@st.cache # Cache data after loading
##def load_data(nrows):
##    data=pd.read_csv(DATA_URL, nrows=nrows)
##    lowercase = lambda x: str(x).lower()
##    data.rename(lowercase, axis='columns', inplace=True)
##    data[DATE_COLUMN]=pd.to_datetime(data[DATE_COLUMN])
##    return data
##
### create loading message
##data_load_state=st.text('Loading data......')
##
### Load 10k rows of data
##data=load_data(10000)
##
### Successful load message
##data_load_state.text('Data load done!...and it\'s cached!..and saves automatically.')
##
##
### view data with button option
##if st.checkbox("Show the raw data"):
##    st.subheader('Raw Data')
##    st.write(data) #should select correct type of render automatically. If not, it can be forced to a specific type (see API)
##
##
### make graph
##st.subheader('Pickups per hour')
##hist_values= np.histogram(
##    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
##st.bar_chart(hist_values)
##
##
### make a map
##st.subheader("Map of pickups")
##st.map(data)
##
### make a better map
##hour_to_filter=17
##filtered_data=data[data[DATE_COLUMN].dt.hour==hour_to_filter]
##st.subheader(f'Map of all pickups at {hour_to_filter}:00')
##st.map(filtered_data)
##
### add a slider
##choose_hour_to_filter=st.slider("hour", 0, 23, 17) # minimum: 0h, maximum: 23h, default = 17h
##filtered_data=data[data[DATE_COLUMN].dt.hour==choose_hour_to_filter]
##st.subheader(f'Map of all pickups at {hour_to_filter}:00')
##st.map(filtered_data)
##
##
##
