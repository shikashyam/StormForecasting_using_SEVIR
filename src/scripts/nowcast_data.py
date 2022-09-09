import h5py
import numpy as np
import os
import gcsfs

filesys=gcsfs.GCSFileSystem(project="sevir-project-bdia",token="cloud_storage_creds.json")
def run(data_path,filename,fileindex):
    file_path = data_path + filename
    
    sevirfile=filesys.open(file_path,'rb')
    data = h5py.File(sevirfile, 'r')
    s = np.s_[fileindex-1:fileindex:fileindex+1]
    vil = data['vil'][s]

    res = {'IN':[],"OUT":[]}
    for i in vil:
        split_data(i, res)
    res["IN"] = np.array(res["IN"])
    res["OUT"] = np.array(res["OUT"])

    return res


def split_data(array, res):
    for i in range(25):
        temp = np.dsplit(array, np.array([i, i + 13, i + 25]))
        res['IN'].append(temp[1])
        res['OUT'].append(temp[2])


