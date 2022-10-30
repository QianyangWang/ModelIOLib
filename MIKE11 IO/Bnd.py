import re

def check_f_path(path):
    if "|" not in path:
        path = "|{}|".format(path)

    return path


class PFS_Object():

    def check_trans(self,value):
        if value == "true" or value == "false":
            value = value
        elif "|" in value:
            value = value
        elif isinstance(value,str):
            value = "'{}'".format(value)
        else:
            value = str(value)
        return value

    #append it into module hdparam (replace the original eval method)
    def rev_check_trans(self,value):
        if "true" in value or "false" in value:
            value = value
        elif "|" in value:
            value = re.findall("\|.*?\|",value)[0]
        else:
            value = eval(value)
        return value

    def extract_values(self,value):
        res = value.split("=")[1]
        res_arr = res.split(",")
        res_arr = [re.findall("^\s*(.+)",i)[0] for i in res_arr]
        res_arr = [self.rev_check_trans(i) for i in res_arr]
        return res_arr


class Sub_Array(PFS_Object):

    def __init__(self,content,data_title):
        self.content = content
        self.data_title = data_title
        if self.content:
            self.scan_bullets()
        else:
            self.data = []

    def scan_bullets(self):
        bullets = self.content.split("\n")
        bullets = [re.findall("^\s*(.+)",i)[0] for i in bullets]
        value_list = []
        for i in bullets:
            name,values = i.split("=")
            values = values.split(",")
            values = [re.findall("^\s*(.+)",i)[0] for i in values]
            values = [self.rev_check_trans(j) for j in values]
            value_list.append(values)
        self.data = value_list

    def write(self,title,level = 3):
        contents = []
        contents.append("{}[{}]\n".format(level * 3 * " ", title))
        for i in self.data:
            row_data = ", ".join([self.check_trans(j) if isinstance(j,str) else str(j) for j in i])
            row = "{}{} = {}\n".format((level + 1) * 3 * " ", self.data_title,row_data)
            contents.append(row)
        contents.append("{}EndSect  // {}\n\n".format(level * 3 * " ", title))
        return contents



class Bnd11_Reader(PFS_Object):

    def __init__(self,path):
        self.contents,self.__contents = self.scan_contents(path)
        self.head = self.read_head()
        self.comment = self.read_comment()
        self.BndCndArrays = []
        self.scan_bnd_cnd_arrays()

    def scan_contents(self, path):
        with open(path) as f:
            settings = f.readlines()
            settings2 = "".join(settings)
        return settings,settings2

    def read_head(self):
        head = self.contents[0:3]
        head.append("\n")
        return head

    def read_comment(self):
        comments = re.findall("Comment = ('.*?')\n",self.__contents)
        return comments[0]

    def scan_bnd_cnd_arrays(self):
        bnd_cnd_arrays = re.findall("\[BndCndArray]\n([\s\S]*?)...EndSect..// BndCndArray",self.__contents)
        for a in bnd_cnd_arrays:
            self.BndCndArrays.append(Bnd_Cnd_Array(a))

    def write(self,path):
        contents = []
        contents.extend(self.head)
        contents.append("[BndCondition]\n")
        contents.append("   Comment = {}\n".format(self.comment))
        for item in self.BndCndArrays:
            bnd_cnd_item = item.write(level = 1)
            contents.extend(bnd_cnd_item)
        contents.append("EndSect  // BndCondition\n\n")

        with open(path,"w") as f:
            f.writelines(contents)

class Bnd_Cnd_Array(PFS_Object):

    def __init__(self,bnd_array):
        self.__contents = bnd_array
        self.BndItems = self.__BndItems()
        self.scan_bnd_items()

    def scan_bnd_items(self):
        bnd_items = re.findall("\[BndItem]\n([\s\S]*?)......EndSect..// BndItem",self.__contents)
        for i in bnd_items:
            self.BndItems.append(Bnd_Item(i))
        self.BndItems.categorize()

    def write(self,level = 1):
        contents = []
        contents.append("{}[BndCndArray]\n".format(level * 3 * " "))
        for item in self.BndItems:
            bnd_item = item.write(level = level + 1)
            contents.extend(bnd_item)
        contents.append("{}EndSect  // BndCndArray\n\n".format(level * 3 * " "))
        return contents

    def __getitem__(self, item):
        return self.BndItems[item]


    class __BndItems():

        def __init__(self):
            self.items = []

        def append(self,item):
            self.items.append(item)

        def categorize(self):
            self.Open = [i for i in self.items if i.BndDescription == 0]
            self.PointSource = [i for i in self.items if i.BndDescription == 1]
            self.DistributedSource = [i for i in self.items if i.BndDescription == 2]
            self.Global = [i for i in self.items if i.BndDescription == 3]
            self.Structures = [i for i in self.items if i.BndDescription == 4]
            self.Closed = [i for i in self.items if i.BndDescription == 5]

        def __len__(self):
            return len(self.items)

        def __getitem__(self, item):
            return self.items[item]


class Bnd_Item(PFS_Object):

    def __init__(self,bnd_item=None):
        if bnd_item:
            self.__contents = bnd_item
            self.scan_bullets()

    def scan_bullets(self):
        DescType = self.extract_values(re.findall("(DescType.*?)\n",self.__contents)[0])
        # DescType important description features
        self.BndDescription = DescType[0]
        self.BndType = DescType[1]
        self.BranchName = DescType[2]
        self.StartChainage = DescType[3]
        self.EndChainage = DescType[4]
        self.GateID = DescType[5]
        self.BndID = DescType[6]

        self.OpenDesc = self.extract_values(re.findall("(OpenDesc.*?)\n",self.__contents)[0])
        self.Dam = self.extract_values(re.findall("(Dam.*?)\n",self.__contents)[0])
        self.Inflow = self.extract_values(re.findall("(Inflow.*?)\n", self.__contents)[0])
        self.ADRR = self.extract_values(re.findall("(ADRR.*?)\n", self.__contents)[0])
        self.QhADM12 = self.extract_values(re.findall("(QhADM12.*?)\n", self.__contents)[0])
        self.AutoCalQh = self.extract_values(re.findall("(AutoCalQh.*?)\n", self.__contents)[0])
        self.BndTS = self.extract_values(re.findall("(BndTS.*?)\n", self.__contents)[0])
        #self.read_sub("FractionArray")
        self._FractionArray = Sub_Array(self.read_sub("FractionArray"),"Fraction")
        self.FractionArray = self._FractionArray.data

        self._HDArray = Sub_Array(self.read_sub("HDArray"),"BndTS")
        self.HDArray = self._HDArray.data
        self._InflowArray = Sub_Array(self.read_sub("InflowArray"),"Inflow")
        self.InflowArray = self._InflowArray.data
        self._QhArray = Sub_Array(self.read_sub("QhArray"),"Qh")
        self.QhArray = self._QhArray.data

        self._ComponentArray = Sub_Array(self.read_sub("ComponentArray"),"Component")
        self.ComponentArray = self._ComponentArray.data


    def read_sub(self,title):
        bnd_cnd_arrays = re.findall("\[{}]\n([\s\S]*?)\s+EndSect..// {}".format(title,title), self.__contents)

        return bnd_cnd_arrays[0]

    def _write_bullets(self,title,data,level):
        row_data = ", ".join([self.check_trans(j) if isinstance(j,str) else str(j) for j in data])
        row = "{}{} = {}\n".format((level) * 3 * " ",title,row_data)
        return row

    def write(self,level = 2):
        contents = []
        contents.append("{}[BndItem]\n".format(level * 3 * " "))
        DescType = (self.BndDescription,self.BndType,self.BranchName,self.StartChainage,self.EndChainage,self.GateID,self.BndID)
        DescType = ", ".join([self.check_trans(j) if isinstance(j,str) else str(j) for j in DescType])
        DescType_r = "{}DescType = {}\n".format((level + 1) * 3 * " ",DescType)
        contents.append(DescType_r)

        OpenDesc_r = self._write_bullets("OpenDesc",self.OpenDesc,level + 1)
        contents.append(OpenDesc_r)
        Dam_r = self._write_bullets("Dam",self.Dam,level + 1)
        contents.append(Dam_r)
        Inflow_r = self._write_bullets("Inflow",self.Inflow,level + 1)
        contents.append(Inflow_r)
        ADRR_r = self._write_bullets("ADRR",self.ADRR,level + 1)
        contents.append(ADRR_r)
        QhADM12_r = self._write_bullets("QhADM12",self.QhADM12,level + 1)
        contents.append(QhADM12_r)
        AutoCalQh_r = self._write_bullets("AutoCalQh",self.AutoCalQh,level + 1)
        contents.append(AutoCalQh_r)
        BndTS_r = self._write_bullets("BndTS",self.BndTS,level + 1)
        contents.append(BndTS_r)

        FractionArray_r = self._FractionArray.write("FractionArray",level+1)
        contents.extend(FractionArray_r)
        HDArray_r = self._HDArray.write("HDArray",level+1)
        contents.extend(HDArray_r)
        InflowArray_r = self._InflowArray.write("InflowArray",level+1)
        contents.extend(InflowArray_r)
        QhArray_r = self._QhArray.write("QhArray",level+1)
        contents.extend(QhArray_r)
        ComponentArray_r = self._ComponentArray.write("ComponentArray",level+1)
        contents.extend(ComponentArray_r)

        contents.append("{}EndSect  // BndItem\n\n".format(level * 3 * " "))

        return contents


class SWMM_Linkage_Bnd_Item(Bnd_Item):

    def __init__(self,reach,hd_ts_file,ad_ts_files = [],component_id = []):
        super().__init__()

        self.BranchName = reach
        self.GateID = ""
        self.BndID = ""

        self.OpenDesc = [0,0]
        self.Dam = [0,0,0]
        if ad_ts_files:
            self.Inflow = ['true','true','false','false']
        else:
            self.Inflow = ['true', 'false', 'false', 'false']
        self.ADRR = ['', 0, 0]
        self.QhADM12 = [2, 1, 0]
        self.AutoCalQh = [0, 0.001, 40]
        self.BndTS = [ 0, '||', 0, 0, '', 0, 1]

        self._FractionArray = Sub_Array(None,"Fraction")
        self.FractionArray = self._FractionArray.data

        self._HDArray = Sub_Array(None,"BndTS")
        self.HDArray = self._HDArray.data
        self._InflowArray = Sub_Array(None,"Inflow")
        self.InflowArray = self._InflowArray.data
        self._QhArray = Sub_Array(None,"Qh")
        self.QhArray = self._QhArray.data

        self._ComponentArray = Sub_Array(None,"Component")
        self.ComponentArray = self._ComponentArray.data

        self.InflowArray.append([0,0,0,check_f_path(hd_ts_file),0,1,"",0,1])
        if ad_ts_files:
            if not component_id:
                component_id = [i+1 for i in range(len(ad_ts_files))]
            for i in range(len(ad_ts_files)):
                row = [component_id[i],0,0,check_f_path(ad_ts_files[i]),0,0, '', 0, 1]
                self.ComponentArray.append(row)



class Point_Source_Item(SWMM_Linkage_Bnd_Item):

    def __init__(self,reach,start_chainage,hd_ts_file,ad_ts_files = [],component_id = []):
        super().__init__(reach,hd_ts_file,ad_ts_files = ad_ts_files,component_id = component_id)
        self.BndDescription = 1
        self.BndType = 0
        self.StartChainage = start_chainage
        self.EndChainage = 0


class Distributed_Source_Item(SWMM_Linkage_Bnd_Item):
    def __init__(self,reach,start_chainage,end_chainage,hd_ts_file,ad_ts_files = [],component_id = []):
        super().__init__(reach,hd_ts_file,ad_ts_files = ad_ts_files,component_id = component_id)
        self.BndDescription = 2
        self.BndType = 2
        self.StartChainage = start_chainage
        self.EndChainage = end_chainage


"""
Inflow = 0, 1.8, 1, |..\..\数据\Dongzhen_shengtai.dfs0|, 1.1, 1, 'inflow', 0, 1
AD boundaries, K-mix, TS Type, File/Value, constant value, unknown (TS = 1, Constant = 0), description, unknown, unknown


bnd = Bnd11_Reader(r"D:\tonghui_model\tonghui_bnd.bnd11")
#bnd.write(r"D:\model\bnd\Bndpython.bnd11")
#bnd.BndCndArrays[0].BndItems[0].write("FractionArray")
for bndi in bnd.BndCndArrays[0].BndItems:
    bndi.Inflow = ['true', 'true', 'false', 'false']
    if "j" in bndi.BndID:
        c1 = [1, 0, 0, '|.\\swmmout_wq\\{}_COD.dfs0|'.format(bndi.BndID), 0, 1, 'SWMM_node', 0, 1]
        c2 = [2, 0, 0, '|.\\swmmout_wq\\{}_NH3N.dfs0|'.format(bndi.BndID), 0, 1, 'SWMM_node', 0, 1]
        c3 = [3, 0, 0, '|.\\swmmout_wq\\{}_TN.dfs0|'.format(bndi.BndID), 0, 1, 'SWMM_node', 0, 1]
        c4 = [4, 0, 0, '|.\\swmmout_wq\\{}_TP.dfs0|'.format(bndi.BndID), 0, 1, 'SWMM_node', 0, 1]
        bndi._ComponentArray.data = [c1,c2,c3,c4]


bnd.write(r"D:\tonghui_model\tonghui_bnd.bnd11")

"""