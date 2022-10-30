import Bnd
import warnings

def update_mike11_bnditem(reach = "",start_chainage = 0,end_chainage = 0,hd_ts_file = "",ad_ts_files = [],component_id = [],bnd_item = None):
    """
    :param reach:
    :param start_chainage:
    :param end_chainage:
    :param hd_ts_file:
    :param ad_ts_files:
    :param component_id:
    :param bnd_item:
    :return:
    """
    if not hd_ts_file and not ad_ts_files:
        return
    if bnd_item:

        # update the original bnd_item
        if hd_ts_file:
            # open the hd calc switch
            bnd_item.Inflow[0] = "true"
            bnd_item.InflowArray[0][3] = check_f_path(hd_ts_file)
        if ad_ts_files:
            # open the ad calc switch
            bnd_item.Inflow[1] = "true"
            # the given bnd_item does not have ad time series
            if not bnd_item.ComponentArray:
                # if: the corresponding component id list is given, the component data will be allocated according to the id list
                # else: the component will be allocated according to the sequence
                if component_id:
                    for i in range(len(ad_ts_files)):
                        # bnd component array format: id, data type {0:concentration,1:bacteria,2:...},
                        # ts type {0:ts file,1:constant}, f_path, constant_value (if the ts type is constant), unknown, ts_info, unknown, unknown
                        component_data = [component_id[i],0,0,check_f_path(ad_ts_files[i]),0,0,'',0,1]
                        bnd_item.ComponentArray.append(component_data)
                else:
                    warnings.warn('The component id list is not given, the MIKE11 ad data series will be automatically\
                     allocated to the components according to the sequence.', UserWarning)
                    for i in range(len(ad_ts_files)):
                        # bnd component array format: id, data type {0:concentration,1:bacteria,2:...},
                        # ts type {0:ts file,1:constant}, f_path, constant_value (if the ts type is constant), unknown, ts_info, unknown, unknown
                        component_data = [i+1,0,0,check_f_path(ad_ts_files[i]),0,0,'',0,1]
                        bnd_item.ComponentArray.append(component_data)
            else:
                if not component_id:
                    warnings.warn('The component id list is not given, the MIKE11 ad data series will be automatically\
                     allocated to the components according to the sequence.', UserWarning)
                    component_id = [i+1 for i in range(len(ad_ts_files))]

                original_c_list = [bnd_item.ComponentArray[i][0] for i in range(len(bnd_item.ComponentArray))]
                for i in range(len(component_id)):
                    # if the original bnd_item has this component
                    if component_id[i] in original_c_list:
                        loc = original_c_list.index(component_id[i])
                        bnd_item.ComponentArray[loc][1] = 0
                        bnd_item.ComponentArray[loc][2] = 0
                        bnd_item.ComponentArray[loc][3] = check_f_path(ad_ts_files[i])
                        bnd_item.ComponentArray[loc][5] = 0
                        bnd_item.ComponentArray[loc][7] = 0
                        bnd_item.ComponentArray[loc][8] = 0
                    # if not, add a new component
                    else:
                        component_data = [component_id[i], 0, 0, check_f_path(ad_ts_files[i]), 0, 0, '', 0, 1]
                        bnd_item.ComponentArray.append(component_data)
    else:
        # create a new bnd_item
        if not reach:
            raise ValueError("A MIKE11 reach name should be given.")
        # point source
        if end_chainage == 0:
            bnd_item = bnuMIKE11.Bnd.Point_Source_Item(reach,start_chainage,hd_ts_file,ad_ts_files,component_id)

        else:
            bnd_item = bnuMIKE11.Bnd.Distributed_Source_Item(reach,start_chainage,end_chainage,hd_ts_file,ad_ts_files,component_id)

    return bnd_item


def check_f_path(path):
    if "|" not in path:
        path = "|{}|".format(path)

    return path

"""
# example
bnd = Bnd.Bnd11_Reader(r"D:\Model\bnd\Bnd_ori.bnd11")
ad_series = [r"D:\Model\AN.dfs0",r"D:\Model\TP.dfs0",r"D:\Model\cod.dfs0",r"D:\Model\AN.dfs0"]
bnd_item = update_mike11_bnditem("Bei1",0,100,hd_ts_file=r"D:\Model\MDL2018.dfs0",ad_ts_files=ad_series,component_id=[2,4,3,1])
bnd.BndCndArrays[0].BndItems.append(bnd_item)
bnd.write(r"D:\Model\bnd\Bnd_new.bnd11")
"""