import math
import os
os.environ['CONDA_DLL_SEARCH_MODIFICATION_ENABLE']="1"
from swmm_api import SwmmInput
from swmm_api.input_file.section_labels import SUBAREAS,INFILTRATION,CONDUITS,LANDUSES,POLLUTANTS,SUBCATCHMENTS,WASHOFF,BUILDUP



def write_n_imperv(params,ininp,mode=0):
    lis_subcatchments = list(ininp[SUBAREAS].keys())
    if mode == 0:
        for subcatchment in lis_subcatchments:
            ininp[SUBAREAS][subcatchment].N_Imperv = params
    else:
        for i in range(len(lis_subcatchments)):
            ininp[SUBAREAS][lis_subcatchments[i]].N_Imperv = params[i]
    return ininp

def write_n_perv(params,ininp,mode=0):
    lis_subcatchments = list(ininp[SUBAREAS].keys())
    if mode == 0:
        for subcatchment in lis_subcatchments:
            ininp[SUBAREAS][subcatchment].N_Perv = params
    else:
        for i in range(len(lis_subcatchments)):
            ininp[SUBAREAS][lis_subcatchments[i]].N_Perv = params[i]
    return ininp


def write_s_perv(params,ininp,mode=0):
    lis_subcatchments = list(ininp[SUBAREAS].keys())
    if mode == 0:
        for subcatchment in lis_subcatchments:
            ininp[SUBAREAS][subcatchment].S_Perv = params
    else:
        for i in range(len(lis_subcatchments)):
            ininp[SUBAREAS][lis_subcatchments[i]].S_Perv = params[i]
    return ininp


def write_s_imperv(params,ininp,mode=0):
    lis_subcatchments = list(ininp[SUBAREAS].keys())
    if mode == 0:
        for subcatchment in lis_subcatchments:
            ininp[SUBAREAS][subcatchment].S_Imperv = params
    else:
        for i in range(len(lis_subcatchments)):
            ininp[SUBAREAS][lis_subcatchments[i]].S_Imperv = params[i]
    return ininp


def write_p_zero(params,ininp,mode=0):
    lis_subcatchments = list(ininp[SUBAREAS].keys())
    if mode == 0:
        for subcatchment in lis_subcatchments:
            ininp[SUBAREAS][subcatchment].PctZero = params
    else:
        for i in range(len(lis_subcatchments)):
            ininp[SUBAREAS][lis_subcatchments[i]].PctZero = params[i]
    return ininp


def write_max_rate(params,ininp,mode=0):
    lis_subcatchments = list(ininp[INFILTRATION].keys())
    if mode == 0:
        for subcatchment in lis_subcatchments:
            ininp[INFILTRATION][subcatchment].MaxRate = params
    else:
        for i in range(len(lis_subcatchments)):
            ininp[INFILTRATION][lis_subcatchments[i]].MaxRate = params[i]
    return ininp


def write_min_rate(params,ininp,mode=0):
    lis_subcatchments = list(ininp[INFILTRATION].keys())
    if mode == 0:
        for subcatchment in lis_subcatchments:
            ininp[INFILTRATION][subcatchment].MinRate = params
    else:
        for i in range(len(lis_subcatchments)):
            ininp[INFILTRATION][lis_subcatchments[i]].MinRate = params[i]
    return ininp


def write_decay(params,ininp,mode=0):
    lis_subcatchments = list(ininp[INFILTRATION].keys())
    if mode == 0:
        for subcatchment in lis_subcatchments:
            ininp[INFILTRATION][subcatchment].Decay = params
    else:
        for i in range(len(lis_subcatchments)):
            ininp[INFILTRATION][lis_subcatchments[i]].Decay = params[i]
    return ininp


def write_ws_width(K,ininp,mode=0):
    lis_subcatchments = list(ininp[SUBCATCHMENTS].keys())
    if mode == 0:
        for subcatchment in lis_subcatchments:
            ininp[SUBCATCHMENTS][subcatchment].Width = K * math.sqrt(10000 * ininp[SUBCATCHMENTS][subcatchment].Area)
    else:
        for i in range(len(lis_subcatchments)):
            ininp[SUBCATCHMENTS][lis_subcatchments[i]].Width = K[i] * math.sqrt(10000 * ininp[SUBCATCHMENTS][lis_subcatchments[i]].Area)
    return ininp


def write_dry_time(params,ininp,mode=0):
    lis_subcatchments = list(ininp[INFILTRATION].keys())
    if mode == 0:
        for subcatchment in lis_subcatchments:
            ininp[INFILTRATION][subcatchment].DryTime = params
    else:
        for i in range(len(lis_subcatchments)):
            ininp[INFILTRATION][lis_subcatchments[i]].DryTime = params[i]
    return ininp


def write_conduit_roughness(params,ininp,mode=0):
    lis_conduits = list(ininp[CONDUITS].keys())
    if mode == 0:
        for conduit in lis_conduits:
            ininp[CONDUITS][conduit].Roughness = params
    else:
        for i in range(len(lis_conduits)):
            ininp[CONDUITS][lis_conduits[i]].Roughness = params[i]
    return ininp


def write_landuse_sweep_interval(param,ininp,landuse_key):
    ininp[LANDUSES][landuse_key].sweep_interval = param
    return ininp


def write_landuse_availability(param,ininp,landuse_key):
    ininp[LANDUSES][landuse_key].availability = param
    return ininp


def write_last_sweep(param,ininp,landuse_key):
    ininp[LANDUSES][landuse_key].last_sweep = param
    return ininp


def write_buildup_params(ininp,landuse_key,pollutant_key,C1=None,C2=None,C3=None):
    if C1:
        ininp[BUILDUP][(landuse_key,pollutant_key)].C1 = C1
    if C2:
        ininp[BUILDUP][(landuse_key, pollutant_key)].C2 = C2
    if C3:
        ininp[BUILDUP][(landuse_key, pollutant_key)].C3 = C3
    return ininp


def write_washoff_params(ininp,landuse_key,pollutant_key,C1=None,C2=None,sweeping_removal=None,BMP_removal=None):
    if C1:
        ininp[WASHOFF][(landuse_key,pollutant_key)].C1 = C1
    if C2:
        ininp[WASHOFF][(landuse_key, pollutant_key)].C2 = C2
    if sweeping_removal:
        ininp[WASHOFF][(landuse_key, pollutant_key)].sweeping_removal = sweeping_removal
    if BMP_removal:
        ininp[WASHOFF][(landuse_key, pollutant_key)].BMP_removal = BMP_removal
    return ininp


def write_buildup_func(ininp,landuse_key,pollutant_key,func_type):
    """
    :param ininp:
    :param landuse_key:
    :param pollutant_key:
    :param func_type: "POW", "EXP", "SAT"
    :return:
    """
    ininp[BUILDUP][(landuse_key, pollutant_key)].func_type = func_type
    return ininp


def write_washoff_func(ininp,landuse_key,pollutant_key,func_type):
    """
    :param ininp:
    :param landuse_key:
    :param pollutant_key:
    :param func_type: "EXP", "RC", "EMC"
    :return:
    """
    ininp[WASHOFF][(landuse_key, pollutant_key)].func_type = func_type
    return ininp


def write_pollutant_params(ininp,pollutant_key,Crain=None,Cgw=None,Crdii=None,Kdecay=None,Co_Frac=None,Cdwf=None,Cinit=None):
    if Crain:
        ininp[POLLUTANTS][pollutant_key].Crain = Crain
    if Cgw:
        ininp[POLLUTANTS][pollutant_key].Cgw = Cgw
    if Crdii:
        ininp[POLLUTANTS][pollutant_key].Crdii = Crdii
    if Kdecay:
        ininp[POLLUTANTS][pollutant_key].Kdecay = Kdecay
    if Co_Frac:
        ininp[POLLUTANTS][pollutant_key].Co_Frac = Co_Frac
    if Cdwf:
        ininp[POLLUTANTS][pollutant_key].Cdwf = Cdwf
    if Cinit:
        ininp[POLLUTANTS][pollutant_key].Cinit = Cinit
    return ininp

"""
ininp = SwmmInput.read_file(r"D:\tonghui_model\thswmm\SWMM0722.inp")
write_ws_width(1.0,ininp)
import inp_io
inp_io.update_inp(ininp,r"D:\tonghui_model\thswmm\SWMM0722.inp")

ininp = SwmmInput.read_file(r"D:\tonghui_model\thswmm\SWMM0806.inp")
print(ininp[BUILDUP][("urban","NH3-N")])
"""