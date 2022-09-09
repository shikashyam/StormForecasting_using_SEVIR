import pandas as pd
import numpy as np
import requests


def CallAPIHitModel():
    cache_df = pd.read_csv('/home/airflow/gcs/data/sample.csv')
    cache_df['image_location']=0
    i = 0
    tryvar=0
    while (i < len(cache_df)):
        
        lat=cache_df['lat'].iloc[i]
        long=cache_df['long'].iloc[i]
        input_json ={
            "latitude": lat,
            "longitude": long,
            "distancelimit":500,
            "date": "2019-06-26",
            "time": "15:32",
            "city": "BARRY",
            "state": "MISSOURI",
            "refresh_flag": "Y",
            "threshold_time": "30",
            "SearchBy": "LatLong"
        }
        print(input_json)
        res=requests.post("https://sevir-project-bdia.ue.r.appspot.com/input/airflow/", json=input_json)
        print("res:",res)
        try:
            print("Cache item number:",i)
            res2=res.json()
            print("res2:",res2)
            if res2['result']=='SUCCESS':
                print("inside if")
                cache_df['image_location'].iloc[i]=res2['detail']
            
        except:
            print("Exception for i:",i)
            tryvar=tryvar+1
            if(tryvar<15):
                i = i - 1
            else:
                break

        i=i+1   

            
        
        
        

    print(cache_df)
    cache_df.to_csv('/home/airflow/gcs/data/sample2.csv',index=False)
            