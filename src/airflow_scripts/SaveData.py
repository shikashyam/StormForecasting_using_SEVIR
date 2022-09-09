import pandas as pd
import gcsfs
from dateutil import tz
import datetime as datetime
import pytz
from google.cloud import storage


def WriteMetadata():
    bucket_name = 'sevir-data-2'
    blob_name = 'sevir_cache.csv'
    client = storage.Client.from_service_account_json('/home/airflow/gcs/data/cloud_storage_creds.json')
    bucket = client.bucket(bucket_name)
    blob = bucket.get_blob(blob_name)
    cache_df = pd.read_csv('/home/airflow/gcs/data/sample2.csv')
    cache_df['file_name']=0
    cache_df['timestamp']=0
    fs = gcsfs.GCSFileSystem(project='sevir-data-bdia', token = '/home/airflow/gcs/data/cloud_storage_creds.json')
    file_list= fs.ls('gs://sevir-data-2/')
    print(file_list)
    print(cache_df)
    for i in range(0,len(cache_df)):
        event_id=cache_df['event_id'].iloc[i]
        filename=[x for x in file_list if str(int(event_id)) in x]
        print(filename)
        cache_df['file_name'].iloc[i]=filename[0]
             
        blob_name2=cache_df['image_location'].iloc[i]
        print(blob_name2) 
        blob2 = bucket.get_blob(blob_name2)
        print(blob2)
        
        utc_time=blob2.updated
        updatedtime=utc_time.astimezone(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')
        cache_df['timestamp'].iloc[i]=updatedtime
        
     
    #print(cache_df)
    print('Got BLOB:',blob)
    cache_df.to_csv('/home/airflow/gcs/data/sevir_cache.csv',index=False)
    blob.upload_from_filename('/home/airflow/gcs/data/sevir_cache.csv')
