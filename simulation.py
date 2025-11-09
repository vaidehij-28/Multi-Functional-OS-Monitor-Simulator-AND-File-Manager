from util import *
from dpallocationalgo import *
from pgreplacementalgo import *
from compactionalgorithms import *
from cpuschedulingalgo import *

# --- Main Menu Handler (Directory Menu) ---
def simmenuoptions():
    settopmargins(True)
    setsimscreenmenus()
    setbottommargins(True)
    
    try:
        simoption = int(input())
    except ValueError:
        clearscn()
        print("Invalid input. Please enter a number.")
        simmenuoptions()
        return

    if simoption == 1:
        clearscn()
        #print(" \nCurrent working directory: ----\n ")
        print("***********************************************************************")
        performdpallocation()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        simmenuoptions()

    elif simoption == 2:
        clearscn()
        #print(" \nChange directory (cd): ----\n ")
        print("***********************************************************************")
        performpgreplacement()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        simmenuoptions()
        
    elif simoption == 3:
        clearscn()
        #print(" \nPerform Compaction: ----\n ")
        print("***********************************************************************")
        performCompaction()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        simmenuoptions()
        
    elif simoption == 4:
        clearscn()
        #print(" \nPerfroming Compaction: ----\n ")
        print("***********************************************************************")
        performcpuscheduling()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        simmenuoptions()    
        
    elif simoption == 100:
        clearscn()
        return 
    else:
        print("you have entered wrong option....")
        clearscn()
        dirmenuoptions()