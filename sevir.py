from datetime import date
from time import time
import streamlit as st
import requests
from PIL import Image
import json
import gcsfs

fs=gcsfs.GCSFileSystem(project="sevir-data-pipeline",token="cloud_storage_creds.json")

st.header("Location based Nowcasting")
latitude = st.text_input("Enter Latitude:")
longitude = st.text_input("Enter Longitude:")
distancelimit = st.text_input("Enter the distance:")
t = st.text_input('Enter the Time:')
d = st.text_input('Enter the Date: ')
city = st.text_input('Enter the City: ')
state = st.text_input('Enter the State: ')

if(latitude==''):
    latitude=None
else:
    latitude=float(latitude)
if(longitude==''):
    longitude=None
else:
    longitude=float(longitude)
if(distancelimit==''):
    distancelimit=None
else:
    distancelimit=float(distancelimit)

data={
  "latitude": latitude,
  "longitude": longitude,
  "distancelimit":distancelimit,
  "date": d,
  "time": t,
  "city": city, 
  "state": state
}
if st.button("Predict"):
    res=requests.post("https://sevir-data-pipeline.uk.r.appspot.com/input/", json=data)
    res2=res.json()
    if res2['detail']=='SUCCESS':
        print("inside if")
        path=fs.open(f'gs://sevir-data/result_plot.png', 'rb')
        image = Image.open(path)
        st.image(image, width=750)
    else:
        st.error('ERROR: ' +res2['detail'])
  
   
