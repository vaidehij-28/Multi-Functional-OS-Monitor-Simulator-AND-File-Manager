# util.py

import os 
# import keyboard  <-- Is line ko hata diya gaya hai.
import time 

# --- Screen & User Input Utilities ---

def clearscn():
    # Windows ke liye 'cls' use karta hai
    if os.name == 'nt':
        _ = os.system('cls')
    # Linux/macOS (posix) ke liye 'clear' use karta hai
    else:
        _ = os.system('clear')
        
def waitforesckey():
    print("")
    # Ab 'escape' ke bajaye 'Enter' key ka intezaar karega
    print("Please press ENTER to continue")
    try:
        # Standard Python input use kiya gaya hai
        input()
    except Exception:
        # Fallback agar koi aur error aaye
        pass

def settopmargins(other):
    if (other):
        print(" ")
        print(" ")
    print(" ")
    print(" ")
    print("                          -----------------------------------------------------------")
 
def setmainscreenmenus():
    print("                          |                       MAIN OPTIONS                       |")
    print("                          |                                                          |")                                      
    print("                          |       1:CPU and Memory information operations            |")
    print("                          |       2:Disk Usage and Network Statistics operations     |")
    print("                          |       3:System & Process related operations              |")
    print("                          |       4:Directory and File Management operations         |")
    print("                          |       5:OS Algorithm Simulations                         |")
    print("                          |       6:Exit                                             |")
    print("                          |                                                          |")

# --- Naya Function Joda Gaya Hai Jisse NameError Theek Ho ---
def setcpuscreenmenus():
    print("                          |         CPU & MEMORY RELATED OPTIONS                     |")
    print("                          |                                                          |")
    print("                          |       1:CPU Times (User/System/Idle)                     |")
    print("                          |       2:System Memory (RAM) Information                  |")
    print("                          |       3:Current CPU Utilization Percentage               |")
    print("                          |       4:CPU Core/Thread Count                            |")
    print("                          |       5:Logged-in Users                                  |")
    print("                          |       6:System Boot Time and Uptime                      |")
    print("                          |       100:Go back to main menu                           |")

def setdirscreenmenus():
    print("                          |     DIRECTORY & FILE MANAGEMENT OPTIONS                  |")
    print("                          |                                                          |")
    print("                          |       1:Get Current Directory                            |")
    print("                          |       2:Change Directory                                 |")
    print("                          |       3:List Directory Content                           |")
    print("                          |       4:Create a New Directory                           |")
    print("                          |       5:Delete a Directory/Folder                        |")
    print("                          |       6:Copy a File                                      |")
    print("                          |       7:Move/Rename a File                               |")
    print("                          |       8:Find Complete Source Path (Absolute)             |")
    print("                          |       100:Go back to main menu                           |")

def setprocscreenmenus():
    print("                          |         PROCESS RELATED OPTIONS                          |")
    print("                          |                                                          |")
    print("                          |       1:List all running process (PID, Name)             |")
    print("                          |       2:Get path of executing Process (by PID)           |")
    print("                          |       3:Get Environment variables of a Process (by PID)  |")
    print("                          |       4:Terminate a Process (by PID/Name)                |")
    print("                          |       5:Get Process details of a Process (by PID)        |")
    print("                          |       6:Suspend/Resume a Process (by PID)                |")
    print("                          |       7:Display Process Tree (Children)                  |")
    #print("                          |       8:Start a New Application/Process                  |")
    print("                          |       100:Go back to main menu                           |")
   
def setdiskscreenmenus():
    print("                          |         DISK & NETWORK RELATED OPTIONS                   |")
    print("                          |                                                          |")                                                 
    print("                          |       1:Disk partitions                                  |")
    print("                          |       2:Disk I/O statistics                              |")
    print("                          |       3:Disk usage                                       |")
    print("                          |       4:Network I/O statistics                           |")
    print("                          |       5:Active Network Connections (Sockets)             |") # <-- Naya Option 5
    print("                          |       100:Go back to main menu                           |")
    
def setsimscreenmenus():
    print("                          |         OS ALGORITHM SIMULATION OPTIONS                  |")
    print("                          |                                                          |")                                                 
    print("                          |       1:Memory Management- Dynamic Partition Algorithm   |")
    print("                          |       2:Memory Management- Page Replacement Algorithm    |")
    print("                          |       3:Disk Management- Disk Compaction Algorithm       |")
    print("                          |       4:CPU - CPU Scheduling Algorithm                   |")
    print("                          |       100:Go back to main menu                           |")

   
def setbottommargins(other):
    print("                          -----------------------------------------------------------")
    print(" ")
    if (other):
        print("Enter any one of the above available options")