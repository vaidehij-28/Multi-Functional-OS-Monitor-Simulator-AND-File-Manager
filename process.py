import os
import psutil 
import time
import subprocess # Naye Process ko start karne ke liye
from util import * # clearscn, waitforesckey, setprocscreenmenus functions ke liye


# --- Helper Function (PID input lene ke liye) ---
def get_pid_input():
    """Helper function to get valid PID input from the user."""
    while True:
        try:
            pid = int(input("Please enter the Process ID (PID) or enter -1 to go back: "))
            if pid == -1:
                clearscn()
                return
            elif psutil.pid_exists(pid):
                return pid
            else:
                print(f"Error: PID {pid} does not exist in the system.")
        except ValueError:
            print("Error: Invalid input. Please enter numbers only.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# --- Option 1: List processes ---
def getprocessnames():
    # Headers print karna
    print(f"{'PID':<6}{'Name':<35}{'Username':<20}")
    print("-" * 61)
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            pid = proc.info.get('pid', 'N/A')
            name = proc.info.get('name', 'N/A')
            
            # Fix for NoneType error
            username = proc.info.get('username')
            if username is None:
                username = "SYSTEM/N/A"
            
            # Print the process data
            print(f"{pid:<6}{name[:33]:<35}{username:<20}")
            
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

# --- Option 2: Executable Path ---
def getprocesspath():
    print("manoj")
    """Displays the process executable path."""
    pid = get_pid_input()
    if pid == -1:
        clearscn()
        return
    if pid is not None:
        try:
            process = psutil.Process(pid)
            print(f"Process Name: {process.name()}")
            print(f"Executable Path (exe): {process.exe()}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            print("Error: Information for this process is not accessible.")
        except Exception as e:
            print(f"Error: {e}")

# --- Option 3: Command Line Arguments ---
def getprocesscmdline():
    print("option3")
    """Displays the command line used to start the process."""
    pid = get_pid_input()
    if pid is not None:
        try:
            proc = psutil.Process(pid)
            cmdline = proc.cmdline()
            print(f"Command line for PID {pid}: {cmdline}")
        except psutil.NoSuchProcess:
            print(f"No process with PID {pid} found.")

# --- Option 4: Environment Variables ---
def getprocessenviron():
    """Displays the process's environment variables."""
    pid = get_pid_input()
    if pid is not None:
        try:
            process = psutil.Process(pid)
            env_vars = process.environ()
            print(f"Process Name: {process.name()}")
            print("Environment Variables (environ):")
            count = 0
            for key, value in env_vars.items():
                if count < 5:
                    print(f"  {key}: {value[:50]}...")
                    count += 1
                else:
                    print("...more Environment Variables exist. (Showing top 5)")
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            print("Error: Information for this process is not accessible.")
        except Exception as e:
            print(f"Error: {e}")

# --- Option 5: Process Kill/Terminate (UPDATED for Name-Based Termination) ---
def terminate_process():
    process_name = input("Enter Process Name to Terminate (e.g., Spotify.exe): ").strip()
    if not process_name:
        print("Error: Process Name cannot be empty.")
        return
    
    found_processes = []
    
    # Process Name ke zariye saare PIDs dhoondhna
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            found_processes.append(proc)
    
    if not found_processes:
        print(f"Error: No processes found with the name '{process_name}'.")
        return
        
    success_count = 0
    
    # Har found process par Terminate action apply karna
    print(f"\nAttempting to TERMINATE {len(found_processes)} instance(s) of '{process_name}'...")

    for process in found_processes:
        try:
            print(f"  Terminating PID {process.info['pid']}...")
            process.terminate() 
            process.wait(timeout=3)
            success_count += 1
            
        except psutil.NoSuchProcess:
            pass # Already terminated ho chuka hoga
        except psutil.AccessDenied:
            print(f"  Warning: Access denied for PID {process.info['pid']} (Skipped).")
        except psutil.TimeoutExpired:
            print(f"  Warning: PID {process.info['pid']} is taking too long to terminate.")
        except Exception as e:
            print(f"  Unexpected Error for PID {process.info['pid']}: {e}")
            
    if success_count > 0:
        print(f"\nSuccess: {success_count} instance(s) of '{process_name}' have been TERMINATED.")
    else:
        print("\nOperation failed for all instances (Check permissions/errors above).")


# --- Option 6: Process Detailed Information ---
def get_detailed_process_info():
    pid = get_pid_input()
    if pid is not None:
        try:
            process = psutil.Process(pid)
            # FIX: 'connections' attribute ko hata diya gaya hai, jisse error aa raha tha.
            info = process.as_dict(attrs=['name', 'exe', 'cmdline', 'cwd', 'status', 'memory_info', 'cpu_percent', 'open_files']) 
            
            print(f"\n--- Detailed Info for PID {pid} ({info.get('name', 'N/A')}) ---")
            
            # Simple details
            print(f"  Name:           {info.get('name', 'N/A')}")
            print(f"  Status:         {info.get('status', 'N/A')}")
            print(f"  CPU %:          {info.get('cpu_percent', 'N/A')}%")
            
            # Memory Details
            mem = info.get('memory_info')
            if mem:
                rss = mem.rss / (1024 * 1024)
                vms = mem.vms / (1024 * 1024)
                print(f"  Memory (RSS):   {rss:.2f} MB")
                print(f"  Memory (VMS):   {vms:.2f} MB")
            
            # Executable Path and Working Dir (cwd)
            print(f"\n  Executable Path: {info.get('exe', 'N/A')}")
            print(f"  Working Dir (CWD): {info.get('cwd', 'N/A')}")
            
            # Open Files (top 3 dikha rahe hain)
            open_files = info.get('open_files')
            if open_files:
                print(f"\n  Open Files ({len(open_files)} total):")
                for item in open_files[:3]:
                    print(f"    - {item.path}")
                if len(open_files) > 3:
                    print(f"    ... and {len(open_files) - 3} more files are open.")
            
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            print("Error: Detailed information for this process is not accessible.")
        except Exception as e:
            # Baaki unexpected errors ko handle karne ke liye
            print(f"Unexpected Error: {e}")

# --- Option 7: Process Priority Change (nice) ---
def change_process_priority():
    """Changes the priority value of a process using Windows Priority Classes."""
    pid = get_pid_input()
    if pid is not None:
        try:
            process = psutil.Process(pid)
            current_nice = process.nice()
            
            # Windows Priority Constants ko ek dictionary mein map karna
            PRIORITY_MAP = {
                'IDLE': psutil.IDLE_PRIORITY_CLASS, # Sabse Kam (64)
                'LOW': psutil.IDLE_PRIORITY_CLASS,
                'BELOW_NORMAL': psutil.BELOW_NORMAL_PRIORITY_CLASS, # Kam (16384)
                'NORMAL': psutil.NORMAL_PRIORITY_CLASS, # Default (32)
                'ABOVE_NORMAL': psutil.ABOVE_NORMAL_PRIORITY_CLASS, # Zyada (32768)
                'HIGH': psutil.HIGH_PRIORITY_CLASS, # Sabse Zyada (128)
                'REALTIME': psutil.REALTIME_PRIORITY_CLASS # Sabse Bada, Warning: System Stability par asar pad sakta hai (256)
            }
            
            # Inverse map for display
            DISPLAY_MAP = {v: k for k, v in PRIORITY_MAP.items()}
            
            # Current priority name nikalo
            current_priority_name = DISPLAY_MAP.get(current_nice, "UNKNOWN")

            print(f"Process Name: {process.name()}")
            print(f"Current Priority: {current_priority_name} (Value: {current_nice})")

            # User se naya priority name input lena
            print("\nAvailable NEW Priorities (Type the name):")
            print(" LOW | NORMAL | HIGH | BELOW_NORMAL | ABOVE_NORMAL")
            
            new_priority_name = input("Enter NEW Priority (e.g., HIGH, NORMAL, LOW): ").upper()
            
            if new_priority_name not in PRIORITY_MAP:
                print("Error: Invalid priority name entered. Please choose from the list.")
                return

            # Naye name se sahi Windows constant value lena
            new_nice = PRIORITY_MAP[new_priority_name]

            # Priority set karna
            process.nice(new_nice)
            
            # Naya priority name nikalna
            new_priority_name_display = DISPLAY_MAP.get(process.nice(), "N/A")
            
            print(f"\nSuccess: Priority of PID {pid} changed to {new_priority_name_display} (Value: {process.nice()}).")
            
        except psutil.AccessDenied:
            print("Error: Access denied. Priority badalne ke liye Admin/Root privileges ki zaroorat hai.")
        except psutil.NoSuchProcess:
            print(f"Error: Process {pid} not found.")
        except Exception as e:
            # Ab yahan [WinError 87] nahi aana chahiye
            print(f"Unexpected Error: {e}")

# --- Option 8: Suspend/Resume Process ---
def suspend_resume_process():
    """Suspends or resumes ALL instances of a process using its name."""
    
    # 1. PID ke bajaye Process Name input lena
    process_name = input("Enter Process Name (e.g., Spotify.exe, chrome.exe): ").strip()
    if not process_name:
        print("Error: Process Name cannot be empty.")
        return
    
    action = input(f"Enter 's' to Suspend ALL '{process_name}' or 'r' to Resume ALL: ").lower()
    
    if action not in ('s', 'r'):
        print("Invalid action entered. Please use 's' or 'r'.")
        return

    found_processes = []
    
    # 2. Process Name ke zariye saare PIDs dhoondhna
    for proc in psutil.process_iter(['pid', 'name']):
        # Ignore case for better matching (spotify.exe == Spotify.exe)
        if proc.info['name'].lower() == process_name.lower():
            found_processes.append(proc)
    
    if not found_processes:
        print(f"Error: No processes found with the name '{process_name}'.")
        return
        
    success_count = 0
    
    # 3. Har found process par action apply karna
    print(f"\nAttempting to {action.upper()} {len(found_processes)} instance(s) of '{process_name}'...")

    for process in found_processes:
        try:
            if action == 's':
                process.suspend()
            elif action == 'r':
                process.resume()
            
            success_count += 1
                
        except psutil.AccessDenied:
            print(f"  Warning: Access denied for PID {process.info['pid']} (Skipped).")
        except Exception as e:
            print(f"  Warning: Could not process PID {process.info['pid']}. Error: {e}")
            
    if success_count > 0:
        print(f"\nSuccess: {success_count} instance(s) of '{process_name}' have been {('SUSPENDED' if action=='s' else 'RESUMED')}.")
    else:
        print("\nOperation failed for all instances (Check permissions/errors above).")


# --- Option 9: Display Process Tree (Children) ---
def get_process_children():
    """Displays the direct child processes of a given PID."""
    pid = get_pid_input()
    if pid is not None:
        try:
            process = psutil.Process(pid)
            children = process.children(recursive=False) # Direct children only
            
            print(f"Process: {process.name()} (PID: {pid})")
            print("\n--- Direct Child Processes ---")
            
            if not children:
                print("(No child processes found)")
                return

            print(f"{'PID':<6}{'Name':<35}{'Status':<15}")
            print("-" * 56)
            for child in children:
                try:
                    print(f"{child.pid:<6}{child.name()[:33]:<35}{child.status():<15}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    print(f"{child.pid:<6}{'N/A':<35}{'N/A':<15}")
            
        except psutil.NoSuchProcess:
            print(f"Error: Process {pid} not found.")
        except psutil.AccessDenied:
            print("Error: Access denied. Cannot access child process information.")
        except Exception as e:
            print(f"Unexpected Error: {e}")

# --- Option 10: Start a New Application/Process (NEW FEATURE) ---
def start_new_process():
    """Starts a new application or process from the command line."""
    
    print("Example: 'notepad.exe', 'cmd.exe', or a full path like 'C:\\Program Files\\app.exe'")
    app_path = input("Enter the command or path of the application to start: ").strip()
    
    if not app_path:
        print("Error: Application path/command cannot be empty.")
        return
        
    try:
        # Popen ka upyog naye process ko background mein start karne ke liye
        # shell=True ka upyog simple commands (notepad, cmd) ke liye zaroori ho sakta hai
        process = subprocess.Popen(app_path, shell=True)
        print(f"\nSuccess: New process '{app_path}' started.")
        print(f"PID: {process.pid}")
        print("Note: The application should now be running in a new window/context.")
        
    except FileNotFoundError:
        print(f"\nError: Application or command '{app_path}' not found.")
    except Exception as e:
        print(f"\nUnexpected Error while starting process: {e}")


# --- Main Menu Handler (Proc Menu) ---

def procmenuoptions():
    settopmargins(True)
    setprocscreenmenus()
    setbottommargins(True)
    
    try:
        processoption = int(input())
    except ValueError:
        clearscn()
        print("Invalid input. Please enter a number.")
        procmenuoptions()
        return

    if processoption == 1:
        clearscn()
        print(" ")
        print("Running processes: ----")
        print(" ")
        print("***********************************************************************")
        getprocessnames()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        procmenuoptions()
    
    elif processoption == 2:
        clearscn()
        print(" ")
        print("Path of process executable: ----")
        print(" ")
        print("***********************************************************************")
        getprocesspath()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        procmenuoptions()

    elif processoption == 3:
        clearscn()
        print(" ")
        print("Process environment variables: ----")
        print(" ")
        print("***********************************************************************")
        getprocessenviron()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        procmenuoptions()
    
    elif processoption == 4:
        clearscn()
        print(" ")
        print("Process Kill/Terminate Operation: ----")
        print(" ")
        print("***********************************************************************")
        terminate_process() 
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        procmenuoptions()
    
    elif processoption == 5:
        clearscn()
        print(" ")
        print("Process Detailed Information: ----")
        print(" ")
        print("***********************************************************************")
        get_detailed_process_info() 
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        procmenuoptions()

    
        
    elif processoption == 6:
        clearscn()
        print(" ")
        print("Suspend (Pause) and Resume Process: ----")
        print(" ")
        print("***********************************************************************")
        suspend_resume_process() 
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        procmenuoptions()

    elif processoption == 7:
        clearscn()
        print(" ")
        print("Display Process Tree (Children): ----")
        print(" ")
        print("***********************************************************************")
        get_process_children()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        procmenuoptions()
        
    # --- Option 10 Handler (NEW) ---
    elif processoption == 8:
        clearscn()
        print(" ")
        print("Start a New Application/Process: ----")
        print(" ")
        print("***********************************************************************")
        start_new_process()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        procmenuoptions()
    
    elif processoption == 11: 
        clearscn()
        print(" \nChange Process Priority: ----\n ")
        print("***********************************************************************")
        change_process_priority() 
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        procmenuoptions()

    elif processoption == 100:
        clearscn()
        return
    else:
        print("you have entered wrong option....")
        clearscn()
        procmenuoptions()


    