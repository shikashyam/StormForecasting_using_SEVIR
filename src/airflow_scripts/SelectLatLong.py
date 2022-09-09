import pandas as pd

def Select50LatLongs():
    print('Selecting 15 Latitudes and Longitudes to save in cache')
    catalog = pd.read_csv("https://raw.githubusercontent.com/MIT-AI-Accelerator/eie-sevir/master/CATALOG.csv")
    catalog=catalog[catalog['event_id'].isna()==False]
    catalog=catalog[catalog['pct_missing']!=0]
    catalog=catalog[(catalog['file_name']=='vil/2019/SEVIR_VIL_STORMEVENTS_2019_0101_0630.h5') | (catalog['file_name']=='vil/2018/SEVIR_VIL_STORMEVENTS_2018_0101_0630.h5')]
    catalog['lat']=round((catalog.llcrnrlat+catalog.urcrnrlat)/2, 6)
    catalog['long']=round((catalog.llcrnrlon+catalog.urcrnrlon)/2, 6)
    df = catalog[['event_id', 'lat', 'long']].head(50)
    df.to_csv('/home/airflow/gcs/data/sample.csv',index=False)