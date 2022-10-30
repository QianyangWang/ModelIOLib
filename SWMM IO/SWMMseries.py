import pandas as pd
import numpy as np
from bnuSWMM import inp_io
from swmm_api.input_file.section_labels import TIMESERIES
import datetime
"""
df = pd.read_excel(r"G:\毕业论文\北京实测数据\水文总站数据\高碑店小时雨量.xlsx")
dates = np.array(df["time"]).flatten()
rain = np.array(df["rain"]).flatten()
dataseries = []
for i in range(len(dates)):
    date = df["time"][i].to_pydatetime()
    data = (date,rain[i])
    dataseries.append(data)
inp = inp_io.open_inp(r"D:\tonghui_model\thswmm\SWMM0722.inp")
inp[TIMESERIES]["gaobeidian"].data = dataseries
inp_io.update_inp(inp,r"D:\tonghui_model\thswmm\SWMM0722.inp")

#####################################
from bnuSWMM import inp_io
from swmm_api.input_file.section_labels import TIMESERIES
inp = inp_io.open_inp(r"D:\tonghui_model\thswmm\SWMM0722.inp")
print(inp[TIMESERIES]["A1052"].data)

import pandas as pd
import numpy as np
import datetime


def get_date_ranges(startdate,enddate,step):
    start = datetime.datetime.strptime(startdate,"%Y/%m/%d %H:%M")
    end = datetime.datetime.strptime(enddate,"%Y/%m/%d %H:%M")
    list_days = []
    while start <= end:
        list_days.append(start)
        start += datetime.timedelta(minutes=step)
    return list_days

df_path = r"G:\毕业论文\北京实测数据\水文总站数据\水文总站日雨量.xlsx"
df = pd.read_excel(df_path)
lejia = df["高碑店"]
rain = np.array(lejia).flatten()
hourly = rain/24

hourly_data = np.zeros(24*len(rain))
for i in range(len(rain)):
    for j in range(24):
        hourly_data[i*24+j] = hourly[i]

dates = np.array(get_date_ranges("2021/01/01 00:00","2021/12/31 23:00",60))
df_src = {"time":dates,"rain":hourly_data}
new_df = pd.DataFrame(df_src)
new_df.to_excel(r"G:\毕业论文\北京实测数据\水文总站数据\高碑店小时雨量.xlsx")
"""
def mike11_df_to_series(inp,series_name,dataframe):
    dataseries = []

    for i in range(len(dataframe)):
        date = dataframe.index[i].to_pydatetime()
        datatuple = (date, dataframe.iloc[i][0])
        dataseries.append(datatuple)

    inp[TIMESERIES][series_name].data = dataseries
    return inp
