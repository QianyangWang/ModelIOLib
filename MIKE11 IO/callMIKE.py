import win32api
import win32event
import win32process
import win32con
from win32com.shell.shell import ShellExecuteEx
from win32com.shell import shellcon

def callexe(f_model, f_sim):

    #ret = win32api.ShellExecute(0,"open",f_model,f_sim,'',1)
    process_info = ShellExecuteEx(nShow=win32con.SW_HIDE,
                                  fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                                  lpVerb='runas',
                                  lpFile=f_model,
                                  lpParameters=f_sim)
    win32event.WaitForSingleObject(process_info['hProcess'], -1)

    ret = win32process.GetExitCodeProcess(process_info['hProcess'])
    #cmd = f_model + " " + f_sim
    #ret = os.system(cmd)

    return  ret



if __name__ == "__main__":
    # example code
    ret = callexe(r"H:\DHI\bin\x64\mike11.exe",r"D:\THcalibpy\process1\tonghuihe.sim11")
    print(ret)

