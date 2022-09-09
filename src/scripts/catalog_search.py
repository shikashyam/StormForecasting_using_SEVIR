#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 14:24:15 2022

@author: shshyam
"""

from importlib.resources import path
import h5py
import math
import boto3
from botocore.handlers import disable_signing
from os import walk
import os
import pandas as pd
from geopy import distance
from geopy import Point
import gcsfs
import numpy as np

fs=gcsfs.GCSFileSystem(project="sevir-project-bdia",token="cloud_storage_creds.json")

def searchincache(lat,long,distlimit):
    print('In Search cache function')
    cache_file=fs.open("gs://sevir-data-2/sevir_cache.csv",'rb')
    cache = pd.read_csv(cache_file)
    myloc=Point(lat,long)
    cache['distance']=cache.apply(lambda row: distancer(row,myloc), axis=1)
    cache=cache[cache["distance"] < int(distlimit)]

    if cache.empty:
        return 'N',None,None,None
    else:
        cache=cache.sort_values(by='distance')
        fileloc=cache.iloc[0]['image_location'] 
        timestamp=cache.iloc[0]['timestamp']     
        print("Searched and found:",lat,":",long,":",fileloc)
        print('LOG : SearchBy : LatLong, Refresh_flag : N, Threshold_time : N/A, Lat :',lat,', Long :', long,', City : N/A, State : N/A, EventID :',float(fileloc.split('.')[0]))
        textnarrative='FUNCTIONALITY NOT SET YET'
    return 'Y',timestamp,fileloc,textnarrative

def searchgeocoordinates(approxlat,approxlong,distlimit):
    print('In search GeoCoordinates function')
    catalog = pd.read_csv("https://raw.githubusercontent.com/MIT-AI-Accelerator/eie-sevir/master/CATALOG.csv")
    catalog=catalog[catalog['event_id'].isna()==False]
    catalog=catalog[catalog['pct_missing']!=0]

    catalog=catalog[(catalog['file_name']=='vil/2019/SEVIR_VIL_STORMEVENTS_2019_0101_0630.h5') | (catalog['file_name']=='vil/2018/SEVIR_VIL_STORMEVENTS_2018_0101_0630.h5')]
    catalog['lat']=(catalog.llcrnrlat+catalog.urcrnrlat)/2
    catalog['long']=(catalog.llcrnrlon+catalog.urcrnrlon)/2
    myloc=Point(approxlat,approxlong)
    catalog['distance']=catalog.apply(lambda row: distancer(row,myloc), axis=1)
    catalog=catalog[catalog["distance"] < int(distlimit)]

    if catalog.empty:
        return None,None,None,None,None,None,None
    else:
        catalog=catalog.sort_values(by='distance')
        lat=catalog.iloc[0]['llcrnrlat']
        long=catalog.iloc[0]['llcrnrlon']
        event_id=catalog.iloc[0]['event_id']
        filename=catalog.iloc[0]['file_name']
        fileidx=catalog.iloc[0]['file_index']
        
        eventsummary,episodesummary=findstormdetails(event_id)
        # if eventsummary==np.nan:
        #     eventsummary=''
        # if episodesummary==np.nan:
        #     episodesummary=''
        return round(lat,6),round(long,6),event_id,filename,fileidx,eventsummary,episodesummary
def findstormdetails(event_id):
    stormdetails_path=fs.open("gs://sevir-data-2/data/storm_details_file.csv",'rb')
    stormdetails = pd.read_csv(stormdetails_path)   
    eventsummary=stormdetails[(stormdetails['EVENT_ID']==event_id)]['EVENT_NARRATIVE'].unique()
    episodesummary=stormdetails[(stormdetails['EVENT_ID']==event_id)]['EPISODE_NARRATIVE'].unique()
    if((np.size(eventsummary)>0)&(np.size(episodesummary)>0)):
        if eventsummary==np.nan:
            eventsummary=''
        if episodesummary==np.nan:
            episodesummary=''
        return eventsummary[0],episodesummary[0]
    else:
        return None,None

def distancer(row,myloc):
    coords_1 = myloc
    coords_2 = (row['lat'], row['long'])
    return distance.distance(coords_1, coords_2).miles


def searchcataloglatlong(lat, long):    
    print("Inside SearchCatalogLatLong")
    event_id,date=get_event_id(lat,long)
    
    if((event_id!='None')):
        filename,fileindex,catalog=get_filename_index(event_id)       
        
        return filename,fileindex[0]
    else:
        return None,None
    
    
def searchcatalogdatetime(date,time,city,state):
    stormdetails_path=fs.open("gs://sevir-data-2/data/storm_details_file.csv",'rb')
    stormdetails = pd.read_csv(stormdetails_path)
    date=date.replace('-','')
    yrmonth=date[0:6]
    day=date[6:8]
    time=time.replace(':','')
    event_id = stormdetails[(stormdetails['BEGIN_YEARMONTH'] == int(yrmonth)) & (stormdetails['BEGIN_DAY']==int(day))& (stormdetails['BEGIN_TIME']==int(time)) & (stormdetails['CZ_NAME']==city)& (stormdetails['STATE']==state)]['EVENT_ID'].unique()
    
    
    if(np.size(event_id)>0):
        filename,fileindex,catalog=get_filename_index(event_id[0])
        eventsummary=stormdetails[(stormdetails['EVENT_ID']==event_id[0])]['EVENT_NARRATIVE'].unique()
        episodesummary=stormdetails[(stormdetails['EVENT_ID']==event_id[0])]['EPISODE_NARRATIVE'].unique()
        if(np.size(fileindex)>0):
            return filename,event_id[0],fileindex[0],eventsummary[0],episodesummary[0]
        else:
            return None,None,None,None,None
    else:
        return None,None,None,None,None
def get_event_id(lat,lon):
    print('inside geteventid')
    df1 = pd.read_csv("https://raw.githubusercontent.com/MIT-AI-Accelerator/eie-sevir/master/CATALOG.csv")
    df1= df1.round({'llcrnrlat':6,'llcrnrlon':6})
    
    
    try:
      date = df1[(df1['llcrnrlon']== lon) & ( df1['llcrnrlat']==lat)]['time_utc'].unique()[0]
      event_id = df1[(df1['llcrnrlon']== lon) & ( df1['llcrnrlat']==lat)]['event_id'].unique()
      
    except:
      print('Lat and long not found')
      date= 'None'
      event_id = 'None'
    if(np.size(event_id)==0):
        date='None'
        event_id='None'
    return event_id,date

def get_filename_index(event_id):
    catlog = pd.read_csv("https://raw.githubusercontent.com/MIT-AI-Accelerator/eie-sevir/master/CATALOG.csv")
    filtered = pd.DataFrame()
    
    filtered = pd.concat([filtered,catlog[(catlog["event_id"] == int(event_id))]])
    allfilenames = filtered['file_name'].unique()
    
    vilpd=catlog[(catlog["event_id"] == int(event_id)) & (catlog['img_type']=='vil') & (catlog['pct_missing']!=0)]
    filename=vilpd['file_name'].unique()
    fileindex = vilpd['file_index'].to_list()
    catalog = pd.read_csv("https://raw.githubusercontent.com/MIT-AI-Accelerator/eie-sevir/master/CATALOG.csv")
    newcatalog=catalog[(catalog['file_name'].isin(allfilenames))]

    
    return filename, fileindex,newcatalog
    
def download_hf(filename):
    resource = boto3.resource('s3')
    resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
    bucket=resource.Bucket('sevir')
    for i in range(len(filename)):
        filename1 = "data/" + filename[i]
        
        return filename[i]
    
def One_Sample_HF(directory,fileindex,filenames):
    newfilepath=''
    for i in range(len(filenames)):
        
        with h5py.File(directory+filenames[i],'r') as hf:
            
            image_type = filenames[i].split('_')[1]
            
            if image_type == "VIL":
                VIL = hf['vil'][int(fileindex[0])] 
    return "sample" 



    
