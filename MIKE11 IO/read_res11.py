import datetime
import time

import numpy as np
from mikeio1d.res1d import Res1D,QueryDataReach
import pandas as pd


def extractWaterLevel(path,branch,chainage,start_time = None,end_time = None):
    df = Res1D(path)
    query = QueryDataReach("Water Level", branch, chainage)
    res = df.read(query)
    data = []
    if start_time and end_time:
        if isinstance(start_time,tuple) or isinstance(start_time, list):
            if len(start_time) != len(end_time):
                raise ValueError("The length of the end_time should equals to which of the start time.")
            else:
                for i in range(len(start_time)):
                    start = datetime.datetime.strptime(start_time[i],"%Y/%m/%d %H:%M:%S")
                    end = datetime.datetime.strptime(end_time[i],"%Y/%m/%d %H:%M:%S")
                    data_series = np.array(res.loc[start:end]).reshape(1,-1)
                    data.append(data_series)
                res = data
        else:
            start = datetime.datetime.strptime(start_time, "%Y/%m/%d %H:%M:%S")
            end = datetime.datetime.strptime(end_time, "%Y/%m/%d %H:%M:%S")
            res = res.loc[start:end]

    return res


def extractDischarge(path,branch,chainage,start_time = None,end_time = None):
    df = Res1D(path)
    query = QueryDataReach("Discharge", branch, chainage)
    res = df.read(query)
    data = []
    if start_time and end_time:
        if isinstance(start_time,tuple) or isinstance(start_time, list):
            if len(start_time) != len(end_time):
                raise ValueError("The length of the end_time should equals to which of the start time.")
            else:
                for i in range(len(start_time)):
                    start = datetime.datetime.strptime(start_time[i],"%Y/%m/%d %H:%M:%S")
                    end = datetime.datetime.strptime(end_time[i],"%Y/%m/%d %H:%M:%S")
                    data_series = np.array(res.loc[start:end]).reshape(1,-1)
                    data.append(data_series)
                res = data
        else:
            start = datetime.datetime.strptime(start_time, "%Y/%m/%d %H:%M:%S")
            end = datetime.datetime.strptime(end_time, "%Y/%m/%d %H:%M:%S")
            res = res.loc[start:end]

    return res

def extractMultiWaterLevel(path,linkage_dict,start_time = None,end_time = None):
    df = Res1D(path)
    links = list(set(linkage_dict))
    data = {}
    for i in links:
        query = QueryDataReach("Water Level", linkage_dict[i][0],  linkage_dict[i][1])
        res = df.read(query)
        if start_time and end_time:
            start = datetime.datetime.strptime(start_time, "%Y/%m/%d %H:%M:%S")
            end = datetime.datetime.strptime(end_time, "%Y/%m/%d %H:%M:%S")
            res = res.loc[start:end]
        data[i] = res
    return data

def extractMultiDepth(path,linkage_dict,start_time = None,end_time = None):
    df = Res1D(path)
    links = list(set(linkage_dict))
    data = {}
    for i in links:
        query = QueryDataReach("Water Level", linkage_dict[i][0],  linkage_dict[i][1])
        res = df.read(query)
        if start_time and end_time:
            start = datetime.datetime.strptime(start_time, "%Y/%m/%d %H:%M:%S")
            end = datetime.datetime.strptime(end_time, "%Y/%m/%d %H:%M:%S")
            res = res.loc[start:end]
        data[i] = res - linkage_dict[i][2]
    return data

"""
path = r"D:\tonghui_model\tonghui_try.res11"
res = extractWaterLevel(path,"Branch1",51151,start_time=["2021/07/10 09:00:00","2021/07/26 20:00:00","2021/08/08 14:00:00","2021/09/03 19:00:00"],
                                                end_time=["2021/07/13 09:00:00","2021/07/28 06:00:00","2021/08/10 09:00:00","2021/09/04 22:00:00"])

print(res)


link_xs_dict = {"Branch1link1":("Branch1",2566.43,101),"Branch1link2":("Branch1",8700,64.404),"Branch1link3":("Branch1",14900,51.06),
                "Branch1link4":("Branch1",17732.3,48.66),"Branch1link5":("Branch1",19757.9,45),"Branch1link6":("Branch1",23384.2,43),
                "Branch1link7":("Branch1",28771.2,35),"Branch1link8":("Branch1",33285.4,33.5),"Branch1link9":("Branch1",36746.2,32),
                "Branch1link10":("Branch1",40329.9,31.32),"Branch1link11":("Branch1",43960.7,28.64),"Branch1link12":("Branch1",47374,26),
                "Branch1link13":("Branch1",49030.5,22.5),"Branch1link14":("Branch1",51151,22.17),"Branch1link15":("Branch1",55271,20.54),
                "Branch1link16":("Branch1",57450,17.53),"Branch6link1":("Branch6",3845,53),"Branch6link2":("Branch6",5700,52),
                "Branch3link1":("Branch3",0,46.9),"Branch3link2":("Branch3",2889.51,46),"Branch3link3":("Branch3",5206,45.5),
                "Branch3link4":("Branch3",7200.71,45),"Branch5link1":("Branch5",6415,36.5),"Branch5link2":("Branch5",11822.6,34.8)}
path = r"D:\tonghui_model\tonghui_try.res11"
data = extractMultiDepth(path,link_xs_dict)['Branch1link14']
"""