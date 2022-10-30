import re


class Param_Object():

    def __init__(self,contents,name = None):
        self.name = name
        self.contents = contents
        self.flag = 0

    def parse_s_param(self, row):
        #row = row.replace(" ", "")
        row = re.findall("^\s*(.+)", row)[0]
        name, value = row.split("=")
        name = re.findall("^\s*(.+)", name)[0].strip()
        value = value.replace("\n", "")
        value = re.findall("^\s*(.+)", value)[0].strip()
        try:
            value = eval(value)
        except:
            value = self.parse_m_param(value)
        return name, value

    def parse_m_param(self, row):
        values = row.split(",")
        values = [re.findall("^\s*(.+)",i)[0] for i in values]
        values = [self.rev_check_trans(j) for j in values]
        if len(values) == 1:
            values = values[0]
        return values

    def read(self, title):
        if self.contents:
            dict_var = {}
            loc1 = self.contents.index("      [{}]\n".format(title))
            loc2 = self.contents.index("      EndSect  // {}\n".format(title))
            params = self.contents[loc1 + 1:loc2]
            for i in range(len(params)):
                if "EndSect" not in params[i]:
                    if self.flag == 0:
                        try:
                            name, value = self.parse_s_param( params[i])
                            dict_var[name] = value
                        except:
                            self.flag = 1
                            title = re.findall("\[(.*?)]", params[i])
                            if title:
                                loc1 = self.contents.index(params[i])
                                loc2 = self.contents.index("         EndSect  // {}\n".format(title[0]))
                                if loc2 > loc1 + 1:
                                    value = Sub_Param_Object(contents=self.contents[loc1 + 1: loc2]).settings
                                else:
                                    value = Sub_Param_Object(contents=None).settings

                                dict_var[title[0]] = value
                    else:
                        title = re.findall("\[(.*?)]", params[i])
                        if title:
                            loc1 = self.contents.index(params[i])
                            loc2 = self.contents.index("         EndSect  // {}\n".format(title[0]))
                            if loc2 > loc1 + 1:
                                value = Sub_Param_Object(contents=self.contents[loc1 + 1: loc2]).settings
                            else:
                                value = Sub_Param_Object(contents=None).settings

                            dict_var[title[0]] = value
            self.flag = 0
            return dict_var
        else:
            return None

    def check_trans(self,value):
        if value == "true" or value == "false":
            value = value
        elif isinstance(value,str):
            if "|" in value:
                value = value
            else:
                value = "'{}'".format(value)
        else:
            value = str(value)
        return value

    def rev_check_trans(self,value):
        if "true" in value or "false" in value:
            value = value
        elif "|" in value:
            value = re.findall("\|.*?\|",value)[0]
        else:
            value = eval(value)
        return value

    def write(self, level, title):
        text = ["{}[{}]\n".format(level * 3 * " ", title)]
        var = eval("self.{}".format(title))
        if var:
            for i in var:
                if not isinstance(var[i],dict):
                    name = i
                    if isinstance(var[i], tuple) or isinstance(var[i], list):
                        value = ", ".join([self.check_trans(j) for j in var[i]])
                    else:
                        if var[i] != '':
                            value = var[i]
                        else:
                            value = "''"
                    row = "{}{} = {}\n".format((level + 1) * 3 * " ", name, value)
                    text.append(row)
                else:
                    subsec = self.write_sub(level + 1, i,var[i])
                    text.extend(subsec)

        text.append("{}EndSect  // {}\n".format(level * 3 * " ", title))
        text.append("\n")
        return text

    def write_sub(self, level, title,var):
        text = ["{}[{}]\n".format(level * 3 * " ", title)]
        if var:
            for i in var:
                if not isinstance(var[i],dict):
                    name = i
                    if isinstance(var[i], tuple) or isinstance(var[i], list):
                        value = ", ".join([self.check_trans(j) for j in var[i]])
                    else:
                        if var[i] != '':
                            value = var[i]
                        else:
                            value = "''"
                    row = "{}{} = {}\n".format((level + 1) * 3 * " ", name, value)
                    text.append(row)
                else:
                    subsec = self.write_sub(level + 1, i,var[i])
                    text.extend(subsec)

        text.append("{}EndSect  // {}\n".format(level * 3 * " ", title))
        text.append("\n")
        return text


class Sub_Param_Object(Param_Object):

    def __init__(self,contents):
        super().__init__(contents)
        self.__contents = contents
        if self.__contents:
            dict_var = {}
            for i in self.__contents:
                name, value = self.parse_s_param(i)
                dict_var[name] = value
            self.settings = dict_var
        else:
            self.settings = {}


class List_Param_Object(Param_Object):

    def __init__(self, contents, name=None):
        super().__init__(contents, name)
        self.__contents = contents
        if self.__contents:
            self.settings = self.read()
        else:
            self.settings = {}

    def read(self,title = None):
        dict_var = {}
        for i in range(len(self.__contents)):
            name,value = self.parse_s_param(self.__contents[i])
            name = name + str(i)
            dict_var[name] = value
        return dict_var

    def write(self, level, title):
        text = ["{}[{}]\n".format(level * 3 * " ", title)]
        var = eval("self.settings")
        if var:
            for i in var:
                if not isinstance(var[i], dict):
                    name = "DATA"
                    if isinstance(var[i], tuple) or isinstance(var[i], list):
                        value = ", ".join([self.check_trans(j) for j in var[i]])
                    else:
                        if var[i] != '':
                            value = var[i]
                        else:
                            value = "''"
                    row = "{}{} = {}\n".format((level + 1) * 3 * " ", name, value)
                    text.append(row)
                else:
                    subsec = self.write_sub(level + 1, i,var[i])
                    text.extend(subsec)

        text.append("{}EndSect  // {}\n".format(level * 3 * " ", title))
        text.append("\n")
        return text


class Param_Reader():

    def __init__(self,path):
        self.contents = self.scan_contents(path)
        self.head = self.read_head()

    def scan_contents(self, path):
        with open(path) as f:
            settings = f.readlines()
        return settings

    def read_head(self):
        head = self.contents[0:3]
        head.append("\n")
        return head

    def find_content_a(self,title):
        loc1 = self.contents.index("   [{}]\n".format(title))
        loc2 = self.contents.index("   EndSect  // {}\n".format(title))
        if self.contents[loc1] == self.contents[loc2]:
            return None
        else:
            return self.contents[loc1:loc2 + 1]

    def find_content_b(self, title):
        loc1 = self.contents.index("   [{}]\n".format(title))
        loc2 = self.contents.index("   EndSect  // {}\n".format(title))
        if self.contents[loc1 + 1] == self.contents[loc2]:
            return None
        else:
            return self.contents[loc1 + 1:loc2]

    def write(self,path):
        pass


class HD11_Reader(Param_Reader):

    def __init__(hd11,path):
        super().__init__(path)
        hd11.Global_Variables = hd11.__Global_Variables(hd11.find_content_b("Global_Variables"),name = "Global_Variables")

        hd11.__InitList = List_Param_Object(hd11.find_content_b("InitList"),name = "InitList")
        hd11.__WindList = List_Param_Object(hd11.find_content_b("WindList"), name="WindList")
        hd11.__BedList = List_Param_Object(hd11.find_content_b("BedList"), name="BedList")
        hd11.__WaveList = List_Param_Object(hd11.find_content_b("WaveList"), name="WaveList")
        hd11.__WaterList = List_Param_Object(hd11.find_content_b("WaterList"), name="WaterList")
        hd11.__FloodList = List_Param_Object(hd11.find_content_b("FloodList"), name="FloodList")
        hd11.__MixingCoefList = List_Param_Object(hd11.find_content_b("MixingCoefList"), name="MixingCoefList")
        hd11.__WaterLevelMarkList = List_Param_Object(hd11.find_content_b("WaterLevelMarkList"), name="WaterLevelMarkList")
        hd11.__BedResistanceToolboxList = List_Param_Object(hd11.find_content_b("BedResistanceToolboxList"), name="BedResistanceToolboxList")
        hd11.__WLCurveList = List_Param_Object(hd11.find_content_b("WLCurveList"), name="WLCurveList")
        hd11.__WLSandBarsList = List_Param_Object(hd11.find_content_b("WLSandBarsList"), name="WLSandBarsList")
        hd11.__Encroachment_Setup = List_Param_Object(hd11.find_content_b("Encroachment_Setup"), name="Encroachment_Setup")
        hd11.__M12ParamList = List_Param_Object(hd11.find_content_b("M12ParamList"), name="M12ParamList")
        hd11.__M12InitList = List_Param_Object(hd11.find_content_b("M12InitList"), name="M12InitList")
        hd11.__QSSContractionExpansionList = List_Param_Object(hd11.find_content_b("QSSContractionExpansionList"), name="QSSContractionExpansionList")
        hd11.__QSSReachLengthsList = List_Param_Object(hd11.find_content_b("QSSReachLengthsList"), name="QSSReachLengthsList")
        hd11.__OutputGridPoints = List_Param_Object(hd11.find_content_b("OutputGridPoints"), name="OutputGridPoints")
        hd11.__LeakageList = List_Param_Object(hd11.find_content_b("LeakageList"), name="LeakageList")

        hd11.InitList = hd11.__InitList.settings
        hd11.WindList = hd11.__WindList.settings
        hd11.BedList = hd11.__BedList.settings
        hd11.WaveList = hd11.__WaveList.settings
        hd11.WaterList = hd11.__WaterList.settings
        hd11.FloodList = hd11.__FloodList.settings
        hd11.MixingCoefList = hd11.__MixingCoefList.settings
        hd11.WaterLevelMarkList = hd11.__WaterLevelMarkList.settings
        hd11.BedResistanceToolboxList = hd11.__BedResistanceToolboxList.settings
        hd11.WLCurveList = hd11.__WLCurveList.settings
        hd11.WLSandBarsList = hd11.__WLSandBarsList.settings
        hd11.Encroachment_Setup = hd11.__Encroachment_Setup.settings
        hd11.M12ParamList = hd11.__M12ParamList.settings
        hd11.M12InitList = hd11.__M12InitList.settings
        hd11.QSSContractionExpansionList = hd11.__QSSContractionExpansionList.settings
        hd11.QSSReachLengthsList = hd11.__QSSReachLengthsList.settings
        hd11.OutputGridPoints = hd11.__OutputGridPoints.settings
        hd11.LeakageList = hd11.__LeakageList.settings

    def write(hd11,path):
        contents = []
        contents.extend(hd11.head)
        contents.append("[MIKE0_HD]\n")
        contents.append("   [Global_Variables]\n")
        gv = hd11.Global_Variables.write(2,"Global_Values")
        dv = hd11.Global_Variables.write(2,"Defalt_Values")
        qs = hd11.Global_Variables.write(2,"Quasi_steady")
        ao = hd11.Global_Variables.write(2,"Add_Output")
        mixing = hd11.Global_Variables.write(2,"MixingCoefficients")
        wlmt = hd11.Global_Variables.write(2,"WaterLevelMarkTitles")
        br = hd11.Global_Variables.write(2,"BedResistTools")
        wlc = hd11.Global_Variables.write(2,"WaterLevelCurve")
        wls = hd11.Global_Variables.write(2,"WaterLevelSandBars")
        en = hd11.Global_Variables.write(2,"Encroachment")
        hb = hd11.Global_Variables.write(2,"Heat_Balance")
        s = hd11.Global_Variables.write(2,"Stratification")
        m12p = hd11.Global_Variables.write(2,"M12Param")
        m12i = hd11.Global_Variables.write(2,"M12Init")
        to = hd11.Global_Variables.write(2,"TextOutput")
        mo = hd11.Global_Variables.write(2,"MapOutput")
        lk = hd11.Global_Variables.write(2,"Leakage")
        temp_l = [gv,dv,qs,ao,mixing,wlmt,br,wlc,wls,en,hb,s,m12p,m12i,to,mo,lk]
        for i in temp_l:
            contents.extend(i)
        contents.append("   EndSect  // Global_Variables\n")
        contents.append("\n")
        ini = hd11.__InitList.write(1,"InitList")
        wnd =  hd11.__WindList.write(1,"WindList")
        bd = hd11.__BedList.write(1,"BedList")
        wv = hd11.__WaveList.write(1,"WaveList")
        wt = hd11.__WaterList.write(1,"WaterList")
        fd = hd11.__FloodList.write(1,"FloodList")
        mx = hd11.__MixingCoefList.write(1, "MixingCoefList")
        wlml = hd11.__WaterLevelMarkList.write(1, "WaterLevelMarkList")
        bdrtl = hd11.__BedResistanceToolboxList.write(1, "BedResistanceToolboxList")
        wlcl = hd11.__WLCurveList.write(1, "WLCurveList")
        wlsb = hd11.__WLSandBarsList.write(1, "WLSandBarsList")
        es = hd11.__Encroachment_Setup.write(1, "Encroachment_Setup")
        m12pl = hd11.__M12ParamList.write(1, "M12ParamList")
        m12il = hd11.__M12InitList.write(1, "M12InitList")
        qss = hd11.__QSSContractionExpansionList.write(1, "QSSContractionExpansionList")
        qssr = hd11.__QSSReachLengthsList.write(1, "QSSReachLengthsList")
        ogrd = hd11.__OutputGridPoints.write(1, "OutputGridPoints")
        lkl = hd11.__LeakageList.write(1, "LeakageList")
        temp_l = [ini,wnd,bd,wv,wt,fd,mx,wlml,bdrtl,wlcl,wlsb,es,m12pl,m12il,qss,qssr,ogrd,lkl]
        for i in temp_l:
            contents.extend(i)
        contents.append("EndSect  // MIKE0_HD\n")
        contents.append("\n")
        with open(path,"w") as f:
            f.writelines(contents)

    class __Global_Variables(Param_Object):

        def __init__(self,contents,name = None):
            super().__init__(contents,name)
            self.Global_Values = self.read("Global_Values")
            self.Defalt_Values = self.read("Defalt_Values")
            self.Quasi_steady = self.read("Quasi_steady")
            self.Add_Output = self.read("Add_Output")
            self.MixingCoefficients = self.read("MixingCoefficients")
            self.WaterLevelMarkTitles = self.read("WaterLevelMarkTitles")
            self.BedResistTools = self.read("BedResistTools")
            self.WaterLevelCurve = self.read("WaterLevelCurve")
            self.WaterLevelSandBars = self.read("WaterLevelSandBars")
            self.Encroachment = self.read("Encroachment")
            self.Heat_Balance = self.read("Heat_Balance")
            self.Stratification = self.read("Stratification")
            self.M12Param = self.read("M12Param")
            self.M12Init = self.read("M12Init")
            self.TextOutput = self.read("TextOutput")
            self.MapOutput = self.read("MapOutput")
            self.Leakage = self.read("Leakage")


class AD11_Reader(Param_Reader):
    def __init__(self, path):
        super().__init__(path)

        self.__Global_Variables = self._Global_Variables(self.find_content_a("Global_Variables"),name = "Global_Variables")
        self.__InitList = List_Param_Object(self.find_content_b("InitList"), name="InitList")
        self.__InitStratified = List_Param_Object(self.find_content_b("InitStratified"), name="InitStratified")
        self.__NonCohesList = List_Param_Object(self.find_content_b("NonCohesList"), name="NonCohesList")
        self.__DecayList = List_Param_Object(self.find_content_b("DecayList"), name="DecayList")
        self.__DispersList = List_Param_Object(self.find_content_b("DispersList"), name="DispersList")
        self.__IceDataList = List_Param_Object(self.find_content_b("IceDataList"), name="IceDataList")
        self.__Cohesive_ST = List_Param_Object(self.find_content_b("Cohesive_ST"), name="Cohesive_ST")
        self.__CompList = List_Param_Object(self.find_content_b("CompList"), name="CompList")
        self.__LayerList = List_Param_Object(self.find_content_b("LayerList"), name="LayerList")
        self.__M12DispersList = List_Param_Object(self.find_content_b("M12DispersList"), name="M12DispersList")

        self.Global_Variables = self.__Global_Variables.settings
        self.InitList = self.__InitList.settings
        self.InitStratified = self.__InitStratified.settings
        self.NonCohesList = self.__NonCohesList.settings
        self.DecayList = self.__DecayList.settings
        self.DispersList = self.__DispersList.settings
        self.IceDataList =  self.__IceDataList.settings
        self.Cohesive_ST = self.__Cohesive_ST.settings
        self.CompList = self.__CompList.settings
        self.LayerList = self.__LayerList.settings
        self.M12DispersList = self.__M12DispersList.settings

    def write(self, path):
        contents = []
        contents.extend(self.head)
        contents.append("[MIKE0_AD]\n")
        gv = self.__Global_Variables.write(1,"Global_Variables")
        contents.extend(gv)

        ini = self.__InitList.write(1,"InitList")
        inis = self.__InitStratified.write(1,"InitStratified")
        nonc = self.__NonCohesList.write(1, "NonCohesList")
        decay = self.__DecayList.write(1, "DecayList")
        disper = self.__DispersList.write(1, "DispersList")
        ice = self.__IceDataList.write(1, "IceDataList")
        coh = self.__Cohesive_ST.write(1, "Cohesive_ST")
        comp = self.__CompList.write(1, "CompList")
        lyr = self.__LayerList.write(1, "LayerList")
        m12d = self.__M12DispersList.write(1, "M12DispersList")
        temp_l = [ini,inis,nonc,decay,disper,ice,coh,comp,lyr,m12d]
        for i in temp_l:
            contents.extend(i)
        contents.append("EndSect  // MIKE0_AD\n")
        contents.append("\n")
        with open(path,"w") as f:
            f.writelines(contents)

    class _Global_Variables(Param_Object):
        def __init__(self, contents, name=None):
            super().__init__(contents, name)
            self.settings = self.read("Global_Variables")

        def read(self, title):
            if self.contents:
                dict_var = {}
                loc1 = self.contents.index("   [{}]\n".format(title))
                loc2 = self.contents.index("   EndSect  // {}\n".format(title))
                params = self.contents[loc1 + 1:loc2]

                for i in range(len(params)):
                    if "EndSect" not in params[i]:
                        if self.flag == 0:
                            try:
                                name, value = self.parse_s_param(params[i])
                                dict_var[name] = value
                            except:
                                self.flag = 1
                                title = re.findall("\[(.*?)]", params[i])
                                if title:
                                    loc1 = self.contents.index(params[i])
                                    loc2 = self.contents.index("      EndSect  // {}\n".format(title[0]))
                                    if loc2 > loc1 + 1:

                                        value = Sub_Param_Object(contents=self.contents[loc1 + 1: loc2]).settings
                                    else:
                                        value = Sub_Param_Object(contents=None).settings
                                    dict_var[title[0]] = value
                        else:
                            title = re.findall("\[(.*?)]", params[i])
                            if title:
                                loc1 = self.contents.index(params[i])
                                loc2 = self.contents.index("      EndSect  // {}\n".format(title[0]))
                                if loc2 > loc1 + 1:
                                    value = Sub_Param_Object(contents=self.contents[loc1 + 1: loc2]).settings
                                else:
                                    value = Sub_Param_Object(contents=None).settings
                                dict_var[title[0]] = value
                self.flag = 0
                return dict_var
            else:
                return None

        def write(self, level, title):
            text = ["{}[{}]\n".format(level * 3 * " ", title)]
            var = eval("self.settings")
            if var:
                for i in var:
                    if not isinstance(var[i], dict):
                        name = i
                        if isinstance(var[i], tuple) or isinstance(var[i], list):
                            value = ", ".join([str(j) if j != '' else "''" for j in var[i]])
                        else:
                            if var[i] != '':
                                value = var[i]
                            else:
                                value = "''"
                        row = "{}{} = {}\n".format((level + 1) * 3 * " ", name, value)
                        text.append(row)
                    else:
                        subsec = self.write_sub(level + 1, i, var[i])
                        text.extend(subsec)

            text.append("{}EndSect  // {}\n".format(level * 3 * " ", title))
            text.append("\n")
            return text



def update_global_resistance(value,hd11_path):

    hd11 = HD11_Reader(hd11_path)
    hd11.Global_Variables.Global_Values['G_resistance'] = value
    hd11.write(hd11_path)


def update_dispersion_coefficient(ad11_path, dispersion_factor = None,exponent=None,min_disp=None,max_disp=None):
    ad11 = AD11_Reader(ad11_path)
    if dispersion_factor:
        ad11.Global_Variables['G_disp_factor'] = dispersion_factor
    if exponent:
        ad11.Global_Variables["G_exponent"] = exponent
    if min_disp:
        ad11.Global_Variables["G_min_disp_coef"] = min_disp
    if max_disp:
        ad11.Global_Variables["G_max_disp_coef"] = max_disp
    ad11.write(ad11_path)


def update_decay(pollutent_key,value,ad11_path):
    """

    :param pollutent_key: The MIKE11 component number starting from 1, if a list -> multiple components
    :param value:
    :param ad11_path:
    :return:
    """
    ad11 = AD11_Reader(ad11_path)
    if isinstance(pollutent_key,int) or isinstance(pollutent_key,str) or isinstance(pollutent_key,float):
        real_key = "DATA{}".format(int(pollutent_key) - 1)
        ad11.DecayList[real_key][1] = value
    else:
        if len(pollutent_key) != len(value):
            raise ValueError("The length of key list should be equal to the length of value list")
        for id,key in enumerate(pollutent_key):
            real_key = "DATA{}".format(int(key) - 1)
            ad11.DecayList[real_key][1] = value[id]
    ad11.write(ad11_path)




