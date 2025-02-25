import pandas as pd
import numpy as np
#np.random.seed(1000)
rstate = 12

#from Common_Tools import wrap_text_excel, expand_cell_excel, grid_excel
#from roctools import full_roc_curve, plot_roc_curve

# import module
import streamlit as st

st.title("Uber pickups in NYC")

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# load the data
data_load_state = st.text("Loading data...")
data = load_data(10000)
data_load_state.text("Loading data... Done!")

# show or hide raw data
if st.checkbox("Show raw data"):
    st.subheader("Raw Data")
    st.write(data)

# histogram to show all the pickups by hour
st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24)
)[0]

st.bar_chart(hist_values)

#st.subheader('Map of all pickups')
#st.map(data)

# show data on a map
hour_to_filter = st.slider('hour', 0, 23,17) #min: 0, max: 24, default: 17
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)