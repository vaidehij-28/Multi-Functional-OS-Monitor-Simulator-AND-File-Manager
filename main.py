from dir import *
from process import *
from cpumem import *
from disknet import *
from simulation import *
    
def mainpage():
    clearscn()
    print('')
    print('')
    print('                              \033[1mMULTI-FUNCTIONAL OS/PROCESS MONITOR & FILE MANAGER')
    settopmargins(False)
    setmainscreenmenus()
    setbottommargins(False)
    
if __name__ == "__main__":
    mainpage()    
    while True:
        print("\n")
        option = input("Enter any one of the above available options (or type 'exit' to quit): ")
        if option.lower() == 'exit':
            print("Exiting the loop.")
            clearscn()
            break  
        else:
            print(f"You entered: {option}")
            if option=="1":
                clearscn()
                cpumenuoptions()
                mainpage()
            elif option=="2":
                clearscn()
                disknetmenuoptions()
                mainpage()
            elif option=="3":
                clearscn()
                procmenuoptions()
                mainpage()
            elif option=="4":
                clearscn()
                dirmenuoptions()
                mainpage()
            elif option=="5":
                clearscn()
                simmenuoptions()
                mainpage()
            else:
                clearscn()
                print("you have entered wrong option....")
                print("Enter one of the correct options or type exit to quit")
                mainpage()