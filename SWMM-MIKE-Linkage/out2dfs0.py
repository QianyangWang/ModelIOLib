import os
import numpy as np
from mikeio import Dfs0
from mikeio.eum import TimeStepUnit, EUMType, EUMUnit, ItemInfo
os.environ['CONDA_DLL_SEARCH_MODIFICATION_ENABLE']="1"
from swmm.toolkit.shared_enum import SystemAttribute,NodeAttribute
import datetime
from pyswmm import Output


def get_date_ranges(start,end,step):
    list_days = []
    while start <= end:
        list_days.append(start)
        start += datetime.timedelta(seconds=step)
    return list_days


def read_swmm_result(path,nodes,start,end,step):

    if type(start) == str:
        try:
            start = datetime.datetime.strptime(start,"%Y-%m-%d %H:%M:%S")
            end = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        except:
            start = datetime.datetime.strptime(start,"%Y/%m/%d %H:%M:%S")
            end = datetime.datetime.strptime(end, "%Y/%m/%d %H:%M:%S")


    time_stamps = get_date_ranges(start,end,step)
    res = []
    with Output(path) as out:
        #data = out.system_result(datetime.datetime(2021, 1, 1, 4))
        for node in nodes:
            ts = out.node_series(node, NodeAttribute.TOTAL_INFLOW, start,end)
            
            node_series = []
            for s in time_stamps[0:-1]:
                node_value = ts[s]
                node_series.append(node_value)
            node_series = np.array(node_series)
            res.append(node_series)
    actual_stamps = time_stamps[0:-1]
    return res,actual_stamps


def swmm_flow2dfs0(path,data_array,timestamp,step):

    dfs = Dfs0()
    dfs.write(path, [data_array], start_time=timestamp, dt=step,items=[ItemInfo("SWMM_node",EUMType.Discharge,EUMUnit.meter_pow_3_per_sec)])


def swmm_pollutant2dfs0(path,data_array,timestamp,step):

    dfs = Dfs0()
    dfs.write(path, [data_array], start_time=timestamp, dt=step,items=[ItemInfo("SWMM_node",EUMType.Concentration,EUMUnit.mg_per_liter)])


def read_swmm_wq_result(path,nodes,start,end,step,pollutant_idx):
    if type(start) == str:
        try:
            start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
            end = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        except:
            start = datetime.datetime.strptime(start, "%Y/%m/%d %H:%M:%S")
            end = datetime.datetime.strptime(end, "%Y/%m/%d %H:%M:%S")

    time_stamps = get_date_ranges(start, end, step)
    res = []
    with Output(path) as out:
        # data = out.system_result(datetime.datetime(2021, 1, 1, 4))
        for node in nodes:
            ts = out.node_series(node, eval("NodeAttribute.POLLUT_CONC_{}".format(pollutant_idx)), start, end)

            node_series = []
            for s in time_stamps[0:-1]:
                node_value = ts[s]
                node_series.append(node_value)
            node_series = np.array(node_series)
            res.append(node_series)
    actual_stamps = time_stamps[0:-1]
    return res, actual_stamps


"""
res,actual_stamps = read_swmm_wq_result(r"D:\tonghui_model\thswmm\SWMM0806.out",["j019","j010"],"2021-05-01 00:00:00","2021-10-31 23:00:00",3600,1)
for i in res[1]:
    print(i)
print(actual_stamps[0])
"""
