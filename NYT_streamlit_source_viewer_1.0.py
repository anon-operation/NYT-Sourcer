import streamlit as st
import pandas as pd
import numpy as np
import pickle
#import plotly.figure_factory as ff
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



st.title("NYT Sourcer App")

filename="TestForGraph"
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
            date=article.pubDate
            count=1
            innerList=[section,url,author,date]
            sources=article.sources
            NLTKs=sources['NLTK']
            for name in NLTKs:
                lower=name.lower()
                print(lower, section, url, date, title, count, sep=",",file=outfile)
        except:
            tryVar=0
    outfile.flush()
    outfile.close()

    df=pd.read_csv('nameDataFrame.csv', sep=',')
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

data_load_state.text('')



########## Graphing
        
st.header("Names in New York Times Stories")
modifyChart=st.checkbox("Click here for more oprtions")
if modifyChart:
    section_selectbox=st.selectbox("What section would you like to see?",
                                   ("All sections", "Health", "U.S.", "Business", "Upshot",
                                    "Magazine", "Briefing", "Podcasts",
                                    "Opinion", "N.Y. Region", "World",
                                    "Climate", "Dining", "Technology",
                                    "Style", "Sports", "Arts"))
    #showAll=st.button('plot all names')
    #plotBySection=st.checkbox('plot by section')
    df3=df
    if section_selectbox=="All sections":
        fig=px.bar(df, x="Name ", y=" Count", color=" Section ",
            hover_data=[" Title ", " Url ", " Date "])
        st.plotly_chart(fig, use_container_width=True)
    else:
        lowercaseSelection=section_selectbox.lower()
        if lowercaseSelection=="u.s.":
            df3=df
            df3=df.convert_dtypes()
            df3=df3[df3[' Section '].str.contains("us")]
            df3=df3[~df3[' Section '].str.contains("ness")]
            fig=px.bar(df3, x="Name ", y=" Count", color=" Section ",
                hover_data=[" Title ", " Url ", " Date "])
            st.plotly_chart(fig, use_container_width=True)
        else:
            df3=df
            df3=df.convert_dtypes()
            df3=df3[df3[' Section '].str.contains(lowercaseSelection)]
            fig=px.bar(df3, x="Name ", y=" Count", color=" Section ",
                    hover_data=[" Title ", " Url ", " Date "])
            st.plotly_chart(fig, use_container_width=True)
else:
    st.text("Chart shows names that appear more than once.")
    df3=df.loc[df.duplicated(subset='Name ', keep=False), :]
    fig=px.bar(df3, x="Name ", y=" Count", color=" Section ",
            hover_data=[" Title ", " Url ", " Date "])
    st.plotly_chart(fig, use_container_width=True)


######### Tabling

showData=st.checkbox("Show the raw data")

if(showData==True):
    matchGraph=st.checkbox("Show data displayed in chart")
    if matchGraph:
        st.subheader('Raw Data from chart')
        name_user_input = st.text_input("Search for a name.", "trump")
        st.dataframe(df3.style.applymap(highlight_name1))
    else:
        st.subheader('Raw Data from entire database')
        name_user_input = st.text_input("Search for a name.", "trump")
        st.dataframe(df.style.applymap(highlight_name1))

    
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
