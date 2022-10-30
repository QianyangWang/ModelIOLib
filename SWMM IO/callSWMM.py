import win32api
import win32event
import win32process
import win32con
from win32com.shell.shell import ShellExecuteEx
from win32com.shell import shellcon

def callexe(f_model, f_sim,f_rpt,fout):
    param = " ".join([f_sim,f_rpt,fout])
    process_info = ShellExecuteEx(nShow=win32con.SW_HIDE,
                                  fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                                  lpVerb='runas',
                                  lpFile=f_model,
                                  lpParameters=param)

    win32event.WaitForSingleObject(process_info['hProcess'], -1)
    ret = win32process.GetExitCodeProcess(process_info['hProcess'])

    #cmd = f_model + " " + f_sim
    #ret = os.system(cmd)

    return  ret

if __name__ == "__main__":

    ret = callexe(r"D:\THcalibpy\process2\swmm5.exe",r"D:\THcalibpy\process2\thswmm\SWMM0722.inp",r"D:\THcalibpy\process2\thswmm\SWMM0722.rpt",r"D:\THcalibpy\process2\thswmm\SWMM0722.out")
    print(ret)
