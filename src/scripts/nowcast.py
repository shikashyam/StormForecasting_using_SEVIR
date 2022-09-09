#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 17:33:49 2022

@author: shshyam
Code to visualize the results from the nowcast model
"""
import os
import time
import io
import h5py
import uuid
from random import randrange
import numpy as np
os.environ["HDF5_USE_FILE_LOCKING"]='FALSE'
import sys
from google.cloud import storage
sys.path.append('../src/')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import matplotlib.patches as patches
import pandas as pd
import matplotlib as mpl
import tensorflow as tf
from matplotlib.colors import LinearSegmentedColormap
import uuid
import gcsfs


filesys=gcsfs.GCSFileSystem(project="sevir-data-bdia",token="cloud_storage_creds.json")


def read_data(filename, rank=0, size=1, end=None, dtype=np.float32, MEAN=33.44, SCALE=47.54):
    x_keys = ['IN']
    y_keys = ['OUT']
    s = np.s_[rank:end:size]
    with h5py.File(filename, mode='r') as hf:
        IN  = hf['IN'][s]
        OUT = hf['OUT'][s]
    IN = (IN.astype(dtype)-MEAN)/SCALE
    OUT = (OUT.astype(dtype)-MEAN)/SCALE
    return IN,OUT

#from nowcast_reader import read_data

def get_cmap(type,encoded=True):
    if type.lower()=='vis':
        cmap,norm = vis_cmap(encoded)
        vmin,vmax=(0,10000) if encoded else (0,1)
    elif type.lower()=='vil':
        cmap,norm=vil_cmap(encoded)
        vmin,vmax=None,None
    elif type.lower()=='ir069':
        cmap,norm=c09_cmap(encoded)
        vmin,vmax=(-8000,-1000) if encoded else (-80,-10)
    elif type.lower()=='lght':
        cmap,norm='hot',None
        vmin,vmax=0,5
    else:
        cmap,norm='jet',None
        vmin,vmax=(-7000,2000) if encoded else (-70,20)

    return cmap,norm,vmin,vmax

def vil_cmap(encoded=True):
    cols=[   [0,0,0],
             [0.30196078431372547, 0.30196078431372547, 0.30196078431372547],
             [0.1568627450980392,  0.7450980392156863,  0.1568627450980392],
             [0.09803921568627451, 0.5882352941176471,  0.09803921568627451],
             [0.0392156862745098,  0.4117647058823529,  0.0392156862745098],
             [0.0392156862745098,  0.29411764705882354, 0.0392156862745098],
             [0.9607843137254902,  0.9607843137254902,  0.0],
             [0.9294117647058824,  0.6745098039215687,  0.0],
             [0.9411764705882353,  0.43137254901960786, 0.0],
             [0.6274509803921569,  0.0, 0.0],
             [0.9058823529411765,  0.0, 1.0]]
    lev = [0.0, 16.0, 31.0, 59.0, 74.0, 100.0, 133.0, 160.0, 181.0, 219.0, 255.0]
    #TODO:  encoded=False
    nil = cols.pop(0)
    under = cols[0]
    over = cols.pop()
    cmap=mpl.colors.ListedColormap(cols)
    cmap.set_bad(nil)
    cmap.set_under(under)
    cmap.set_over(over)
    norm = mpl.colors.BoundaryNorm(lev, cmap.N)
    return cmap,norm
       
    
def vis_cmap(encoded=True):
    cols=[[0,0,0],
             [0.0392156862745098, 0.0392156862745098, 0.0392156862745098],
             [0.0784313725490196, 0.0784313725490196, 0.0784313725490196],
             [0.11764705882352941, 0.11764705882352941, 0.11764705882352941],
             [0.1568627450980392, 0.1568627450980392, 0.1568627450980392],
             [0.19607843137254902, 0.19607843137254902, 0.19607843137254902],
             [0.23529411764705882, 0.23529411764705882, 0.23529411764705882],
             [0.27450980392156865, 0.27450980392156865, 0.27450980392156865],
             [0.3137254901960784, 0.3137254901960784, 0.3137254901960784],
             [0.35294117647058826, 0.35294117647058826, 0.35294117647058826],
             [0.39215686274509803, 0.39215686274509803, 0.39215686274509803],
             [0.43137254901960786, 0.43137254901960786, 0.43137254901960786],
             [0.47058823529411764, 0.47058823529411764, 0.47058823529411764],
             [0.5098039215686274, 0.5098039215686274, 0.5098039215686274],
             [0.5490196078431373, 0.5490196078431373, 0.5490196078431373],
             [0.5882352941176471, 0.5882352941176471, 0.5882352941176471],
             [0.6274509803921569, 0.6274509803921569, 0.6274509803921569],
             [0.6666666666666666, 0.6666666666666666, 0.6666666666666666],
             [0.7058823529411765, 0.7058823529411765, 0.7058823529411765],
             [0.7450980392156863, 0.7450980392156863, 0.7450980392156863],
             [0.7843137254901961, 0.7843137254901961, 0.7843137254901961],
             [0.8235294117647058, 0.8235294117647058, 0.8235294117647058],
             [0.8627450980392157, 0.8627450980392157, 0.8627450980392157],
             [0.9019607843137255, 0.9019607843137255, 0.9019607843137255],
             [0.9411764705882353, 0.9411764705882353, 0.9411764705882353],
             [0.9803921568627451, 0.9803921568627451, 0.9803921568627451],
             [0.9803921568627451, 0.9803921568627451, 0.9803921568627451]]
    lev=np.array([0.  , 0.02, 0.04, 0.06, 0.08, 0.1 , 0.12, 0.14, 0.16, 0.2 , 0.24,
       0.28, 0.32, 0.36, 0.4 , 0.44, 0.48, 0.52, 0.56, 0.6 , 0.64, 0.68,
       0.72, 0.76, 0.8 , 0.9 , 1.  ])
    if encoded:
        lev*=1e4
    nil = cols.pop(0)
    under = cols[0]
    over = cols.pop()
    cmap=mpl.colors.ListedColormap(cols)
    cmap.set_bad(nil)
    cmap.set_under(under)
    cmap.set_over(over)
    norm = mpl.colors.BoundaryNorm(lev, cmap.N)
    return cmap,norm


def ir_cmap(encoded=True):
    cols=[[0,0,0],[1.0, 1.0, 1.0],
     [0.9803921568627451, 0.9803921568627451, 0.9803921568627451],
     [0.9411764705882353, 0.9411764705882353, 0.9411764705882353],
     [0.9019607843137255, 0.9019607843137255, 0.9019607843137255],
     [0.8627450980392157, 0.8627450980392157, 0.8627450980392157],
     [0.8235294117647058, 0.8235294117647058, 0.8235294117647058],
     [0.7843137254901961, 0.7843137254901961, 0.7843137254901961],
     [0.7450980392156863, 0.7450980392156863, 0.7450980392156863],
     [0.7058823529411765, 0.7058823529411765, 0.7058823529411765],
     [0.6666666666666666, 0.6666666666666666, 0.6666666666666666],
     [0.6274509803921569, 0.6274509803921569, 0.6274509803921569],
     [0.5882352941176471, 0.5882352941176471, 0.5882352941176471],
     [0.5490196078431373, 0.5490196078431373, 0.5490196078431373],
     [0.5098039215686274, 0.5098039215686274, 0.5098039215686274],
     [0.47058823529411764, 0.47058823529411764, 0.47058823529411764],
     [0.43137254901960786, 0.43137254901960786, 0.43137254901960786],
     [0.39215686274509803, 0.39215686274509803, 0.39215686274509803],
     [0.35294117647058826, 0.35294117647058826, 0.35294117647058826],
     [0.3137254901960784, 0.3137254901960784, 0.3137254901960784],
     [0.27450980392156865, 0.27450980392156865, 0.27450980392156865],
     [0.23529411764705882, 0.23529411764705882, 0.23529411764705882],
     [0.19607843137254902, 0.19607843137254902, 0.19607843137254902],
     [0.1568627450980392, 0.1568627450980392, 0.1568627450980392],
     [0.11764705882352941, 0.11764705882352941, 0.11764705882352941],
     [0.0784313725490196, 0.0784313725490196, 0.0784313725490196],
     [0.0392156862745098, 0.0392156862745098, 0.0392156862745098],
     [0.0, 0.803921568627451, 0.803921568627451]]
    lev=np.array([-110. , -105.2,  -95.2,  -85.2,  -75.2,  -65.2,  -55.2,  -45.2,
        -35.2,  -28.2,  -23.2,  -18.2,  -13.2,   -8.2,   -3.2,    1.8,
          6.8,   11.8,   16.8,   21.8,   26.8,   31.8,   36.8,   41.8,
         46.8,   51.8,   90. ,  100. ])
    if encoded:
        lev*=1e2
    nil = cols.pop(0)
    under = cols[0]
    over = cols.pop()
    cmap=mpl.colors.ListedColormap(cols)
    cmap.set_bad(nil)
    cmap.set_under(under)
    cmap.set_over(over)
    norm = mpl.colors.BoundaryNorm(lev, cmap.N)
    return cmap,norm         


def c09_cmap(encoded=True):
    cols=[
    [1.000000, 0.000000, 0.000000],
    [1.000000, 0.031373, 0.000000],
    [1.000000, 0.062745, 0.000000],
    [1.000000, 0.094118, 0.000000],
    [1.000000, 0.125490, 0.000000],
    [1.000000, 0.156863, 0.000000],
    [1.000000, 0.188235, 0.000000],
    [1.000000, 0.219608, 0.000000],
    [1.000000, 0.250980, 0.000000],
    [1.000000, 0.282353, 0.000000],
    [1.000000, 0.313725, 0.000000],
    [1.000000, 0.349020, 0.003922],
    [1.000000, 0.380392, 0.003922],
    [1.000000, 0.411765, 0.003922],
    [1.000000, 0.443137, 0.003922],
    [1.000000, 0.474510, 0.003922],
    [1.000000, 0.505882, 0.003922],
    [1.000000, 0.537255, 0.003922],
    [1.000000, 0.568627, 0.003922],
    [1.000000, 0.600000, 0.003922],
    [1.000000, 0.631373, 0.003922],
    [1.000000, 0.666667, 0.007843],
    [1.000000, 0.698039, 0.007843],
    [1.000000, 0.729412, 0.007843],
    [1.000000, 0.760784, 0.007843],
    [1.000000, 0.792157, 0.007843],
    [1.000000, 0.823529, 0.007843],
    [1.000000, 0.854902, 0.007843],
    [1.000000, 0.886275, 0.007843],
    [1.000000, 0.917647, 0.007843],
    [1.000000, 0.949020, 0.007843],
    [1.000000, 0.984314, 0.011765],
    [0.968627, 0.952941, 0.031373],
    [0.937255, 0.921569, 0.050980],
    [0.901961, 0.886275, 0.074510],
    [0.870588, 0.854902, 0.094118],
    [0.835294, 0.823529, 0.117647],
    [0.803922, 0.788235, 0.137255],
    [0.772549, 0.756863, 0.160784],
    [0.737255, 0.725490, 0.180392],
    [0.705882, 0.690196, 0.200000],
    [0.670588, 0.658824, 0.223529],
    [0.639216, 0.623529, 0.243137],
    [0.607843, 0.592157, 0.266667],
    [0.572549, 0.560784, 0.286275],
    [0.541176, 0.525490, 0.309804],
    [0.509804, 0.494118, 0.329412],
    [0.474510, 0.462745, 0.349020],
    [0.752941, 0.749020, 0.909804],
    [0.800000, 0.800000, 0.929412],
    [0.850980, 0.847059, 0.945098],
    [0.898039, 0.898039, 0.964706],
    [0.949020, 0.949020, 0.980392],
    [1.000000, 1.000000, 1.000000],
    [0.964706, 0.980392, 0.964706],
    [0.929412, 0.960784, 0.929412],
    [0.890196, 0.937255, 0.890196],
    [0.854902, 0.917647, 0.854902],
    [0.815686, 0.894118, 0.815686],
    [0.780392, 0.874510, 0.780392],
    [0.745098, 0.850980, 0.745098],
    [0.705882, 0.831373, 0.705882],
    [0.670588, 0.807843, 0.670588],
    [0.631373, 0.788235, 0.631373],
    [0.596078, 0.764706, 0.596078],
    [0.560784, 0.745098, 0.560784],
    [0.521569, 0.721569, 0.521569],
    [0.486275, 0.701961, 0.486275],
    [0.447059, 0.678431, 0.447059],
    [0.411765, 0.658824, 0.411765],
    [0.376471, 0.635294, 0.376471],
    [0.337255, 0.615686, 0.337255],
    [0.301961, 0.592157, 0.301961],
    [0.262745, 0.572549, 0.262745],
    [0.227451, 0.549020, 0.227451],
    [0.192157, 0.529412, 0.192157],
    [0.152941, 0.505882, 0.152941],
    [0.117647, 0.486275, 0.117647],
    [0.078431, 0.462745, 0.078431],
    [0.043137, 0.443137, 0.043137],
    [0.003922, 0.419608, 0.003922],
    [0.003922, 0.431373, 0.027451],
    [0.003922, 0.447059, 0.054902],
    [0.003922, 0.462745, 0.082353],
    [0.003922, 0.478431, 0.109804],
    [0.003922, 0.494118, 0.137255],
    [0.003922, 0.509804, 0.164706],
    [0.003922, 0.525490, 0.192157],
    [0.003922, 0.541176, 0.215686],
    [0.003922, 0.556863, 0.243137],
    [0.007843, 0.568627, 0.270588],
    [0.007843, 0.584314, 0.298039],
    [0.007843, 0.600000, 0.325490],
    [0.007843, 0.615686, 0.352941],
    [0.007843, 0.631373, 0.380392],
    [0.007843, 0.647059, 0.403922],
    [0.007843, 0.662745, 0.431373],
    [0.007843, 0.678431, 0.458824],
    [0.007843, 0.694118, 0.486275],
    [0.011765, 0.705882, 0.513725],
    [0.011765, 0.721569, 0.541176],
    [0.011765, 0.737255, 0.568627],
    [0.011765, 0.752941, 0.596078],
    [0.011765, 0.768627, 0.619608],
    [0.011765, 0.784314, 0.647059],
    [0.011765, 0.800000, 0.674510],
    [0.011765, 0.815686, 0.701961],
    [0.011765, 0.831373, 0.729412],
    [0.015686, 0.843137, 0.756863],
    [0.015686, 0.858824, 0.784314],
    [0.015686, 0.874510, 0.807843],
    [0.015686, 0.890196, 0.835294],
    [0.015686, 0.905882, 0.862745],
    [0.015686, 0.921569, 0.890196],
    [0.015686, 0.937255, 0.917647],
    [0.015686, 0.952941, 0.945098],
    [0.015686, 0.968627, 0.972549],
    [1.000000, 1.000000, 1.000000]]
    
    return ListedColormap(cols),None


## 
# Functions for plotting results
##

norm = {'scale':47.54,'shift':33.44}
hmf_colors = np.array( [
    [82,82,82], 
    [252,141,89],
    [255,255,191],
    [145,191,219]
])/255

# Model that implements persistence forecast that just repeasts last frame of input
class persistence:
    def predict(self,x_test):
        return np.tile(x_test[:,:,:,-1:],[1,1,1,12])

def plot_hit_miss_fa(ax,y_true,y_pred,thres):
    mask = np.zeros_like(y_true)
    mask[np.logical_and(y_true>=thres,y_pred>=thres)]=4
    mask[np.logical_and(y_true>=thres,y_pred<thres)]=3
    mask[np.logical_and(y_true<thres,y_pred>=thres)]=2
    mask[np.logical_and(y_true<thres,y_pred<thres)]=1
    cmap=ListedColormap(hmf_colors)
    ax.imshow(mask,cmap=cmap)


def visualize_result(models,x_test,y_test,idx,event_id,labels):
    fs=10
    idx=randrange(14)
    client = storage.Client.from_service_account_json('cloud_storage_creds.json')
    bucket = client.bucket('sevir-data-2')
    print('IN VISUALIZE RESULTS FUNCTION: event_id is',event_id)
    timeprint=time.strftime("%Y%m%d-%H%M%S")
    
    resfilename=str(int(event_id))+'.png'
    blob = bucket.blob(resfilename)
    cmap_dict = lambda s: {'cmap':get_cmap(s,encoded=True)[0],
                           'norm':get_cmap(s,encoded=True)[1],
                           'vmin':get_cmap(s,encoded=True)[2],
                           'vmax':get_cmap(s,encoded=True)[3]}

    fig,ax = plt.subplots(12,7,figsize=(24,16),gridspec_kw={'width_ratios': [1,0.2,1,0.2,1,1,1]})
    for i in range(1,13):
        xt = x_test[idx,:,:,i]*norm['scale']+norm['shift']
        ax[(i-1)][0].imshow(xt,**cmap_dict('vil'))
    ax[0][0].set_title('Current Data',fontsize=fs)
    
    pers = persistence().predict(x_test[idx:idx+1])
    pers = pers*norm['scale']+norm['shift']
    x_test = x_test[idx:idx+1]
    y_test = y_test[idx:idx+1]*norm['scale']+norm['shift']
    y_preds=[]
    for i,m in enumerate(models):
        yp = m.predict(x_test)
        if isinstance(yp,(list,)):
            yp=yp[0]
        y_preds.append(yp*norm['scale']+norm['shift'])
    
    for i in range(0,12):
        ax[i][2].imshow(y_test[0,:,:,i],**cmap_dict('vil'))
    ax[0][2].set_title('Nowcasting Data',fontsize=fs)
    
    # Plot Persistence
    for i in range(0,12):
        plot_hit_miss_fa(ax[i][4],y_test[0,:,:,i],pers[0,:,:,i],74)
    ax[0][4].set_title('Backtesting Hits and Misses',fontsize=fs)
    
    for k,m in enumerate(models):
        for i in range(0,12):
            ax[i][5+2*k].imshow(y_preds[k][0,:,:,i],**cmap_dict('vil'))
            plot_hit_miss_fa(ax[i][5+2*k+1],y_test[0,:,:,i],y_preds[k][0,:,:,i],74)

        ax[0][5+2*k].set_title(labels[k],fontsize=fs)
        ax[0][5+2*k+1].set_title(labels[k]+'\nBacktesting Model Scores',fontsize=fs)
        
    for j in range(len(ax)):
        for i in range(len(ax[j])):
            ax[j][i].xaxis.set_ticks([])
            ax[j][i].yaxis.set_ticks([])
    for i in range(12):
        ax[i][1].set_visible(False)
    for i in range(12):
        ax[i][3].set_visible(False)
    ax[0][0].set_ylabel('-55 Minutes')
    ax[1][0].set_ylabel('-50 Minutes')
    ax[2][0].set_ylabel('-45 Minutes')
    ax[3][0].set_ylabel('-40 Minutes')
    ax[4][0].set_ylabel('-35 Minutes')
    ax[5][0].set_ylabel('-30 Minutes')
    ax[6][0].set_ylabel('-25 Minutes')
    ax[7][0].set_ylabel('-20 Minutes')
    ax[8][0].set_ylabel('-15 Minutes')
    ax[9][0].set_ylabel('-10 Minutes')
    ax[10][0].set_ylabel('-5 Minutes')
    ax[11][0].set_ylabel(' 0 Minutes')
    ax[0][2].set_ylabel('+5 Minutes')
    ax[1][2].set_ylabel('+10 Minutes')
    ax[2][2].set_ylabel('+15 Minutes')
    ax[3][2].set_ylabel('+20 Minutes')
    ax[4][2].set_ylabel('+25 Minutes')
    ax[5][2].set_ylabel('+30 Minutes')
    ax[6][2].set_ylabel('+35 Minutes')
    ax[7][2].set_ylabel('+40 Minutes')
    ax[8][2].set_ylabel('+45 Minutes')
    ax[9][2].set_ylabel('+50 Minutes')
    ax[10][2].set_ylabel('+55 Minutes')
    ax[11][2].set_ylabel('+60 Minutes')

    
    legend_elements = [Patch(facecolor=hmf_colors[1], edgecolor='k', label='False Alarm'),
                    Patch(facecolor=hmf_colors[2], edgecolor='k', label='Miss'),
                    Patch(facecolor=hmf_colors[3], edgecolor='k', label='Hit')]
    ax[-1][-1].legend(handles=legend_elements, loc='lower right', bbox_to_anchor= (-5.4, -.35), 
                            ncol=5, borderaxespad=0, frameon=False, fontsize='16')
    plt.subplots_adjust(hspace=0.05, wspace=0.05)
    buf=io.BytesIO()
    fig.savefig(buf, bbox_inches='tight',fomat='png')
    
    blob.upload_from_string(buf.getvalue(),content_type='image/png')

    buf.close()

    return resfilename
    
  
    
def plot_results(res,testing_file,idxin,event_id):

    gan_file=filesys.open(f"gs://sevir-data-2/data/gan_generator.h5",'rb')
    gan_data=h5py.File(gan_file,'r')

    gan_model = tf.keras.models.load_model(gan_data,compile=False,custom_objects={"tf": tf})   

    idx=idxin
    
    event_id=event_id

    print('InPlot results : event ID is:',event_id)
    fig=visualize_result([gan_model],res['IN'],res['OUT'],idx,event_id,labels=['cGAN+MAE Model'])
    
    return fig
