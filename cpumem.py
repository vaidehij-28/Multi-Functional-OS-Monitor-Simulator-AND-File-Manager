# cpumem.py

from util import * 
import psutil
import datetime # Import for handling time/dates
from chart import *

# --- Helper Functions for CPU/Memory ---

# Option 1: CPU Times
def cputimes():
    cputime = psutil.cpu_times()
    print("--- CPU Times ---")
    print(f"Time spent by user: {cputime.user} seconds")
    print(f"Time spent by system: {cputime.system} seconds")
    print(f"Time spent idling: {cputime.idle} seconds")

# Option 2: System Memory (RAM) Information
def sysmemory():
    print("HERE")
    vmem = psutil.virtual_memory()
    print("--- System Memory (RAM) Information ---")
    print(f"Total: {vmem.total / (1024**3):.2f} GB")
    print(f"Available: {vmem.available / (1024**3):.2f} GB")
    print(f"Used: {vmem.used / (1024**3):.2f} GB")
    print(f"Percentage Used: {vmem.percent}%")
    sizes = [vmem.used / (1024**3), vmem.available / (1024**3)]
    labels = ['Used', 'Free']
    #getpiechart(sizes, labels, 'System Memory Information')
    def get_sizes():
        v = psutil.virtual_memory()
        return [v.used / (1024**3), v.available / (1024**3)]
        
    getpiechart_live(get_sizes, labels, refresh_rate=2)

# Option 3: CPU Utilization Percentage
def cpu_utilization():
    # interval=1 se 1 second ka average dikhega
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"Current CPU Utilization: {cpu_percent}%")
    # Live line chart for CPU utilization
    plt.ion()
    fig, ax = plt.subplots()
    x_vals, y_vals = [], []

    try:
        for i in range(30):  # monitor for 30 seconds
            if not plt.fignum_exists(fig.number):
                break
            percent = psutil.cpu_percent(interval=1)
            x_vals.append(i)
            y_vals.append(percent)
            ax.clear()
            ax.plot(x_vals, y_vals, marker='o', color='blue')
            ax.set_ylim(0, 100)
            ax.set_xlabel('Seconds')
            ax.set_ylabel('CPU Usage (%)')
            ax.set_title('Live CPU Utilization')
            plt.draw()
            plt.pause(0.1)
    except KeyboardInterrupt:
        print("\nStopped live CPU chart.")

# Option 4: CPU Core/Thread Count
def cpu_count_info():
    physical_cores = psutil.cpu_count(logical=False)
    logical_cores = psutil.cpu_count(logical=True)
    print("--- CPU Count Information ---")
    print(f"Physical Cores (Actual CPUs): {physical_cores}")
    print(f"Logical Cores (Threads/Virtual): {logical_cores}")
    
    # Bar chart
    plt.bar(['Physical Cores', 'Logical Cores'], [physical_cores, logical_cores], color=['#FF6347','#90EE90'])
    plt.title("CPU Core Count")
    plt.ylabel("Number of Cores")
    plt.show()

# Option 5: Logged-in Users
def logged_in_users():
    users = psutil.users()
    if not users:
        print("No users currently logged in.")
        return
    
    print(f"{'Name':<15}{'Terminal':<15}{'Since':<20}")
    print("-" * 50)
    for user in users:
        login_time = datetime.datetime.fromtimestamp(user.started).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{user.name:<15}{user.terminal or 'N/A':<15}{login_time:<20}")

# Option 6: System Boot Time and Uptime
def system_boot_time_and_uptime():
    boot_time_timestamp = psutil.boot_time()
    boot_time = datetime.datetime.fromtimestamp(boot_time_timestamp)
    
    current_time = datetime.datetime.now()
    uptime_duration = current_time - boot_time
    
    print("--- System Boot Time and Uptime ---")
    print(f"System Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"System Uptime: {uptime_duration}")
    
    total_hours = 24
    used_hours = uptime_duration.total_seconds() / 3600
    remaining_hours = max(total_hours - used_hours, 0)
    plt.pie([used_hours, remaining_hours], labels=['Uptime','Remaining Today'], autopct='%1.1f h', startangle=90, colors=['#FF6347','#90EE90'])
    plt.title("System Uptime Today")
    plt.axis('equal')
    plt.show()

# --- Main Menu Handler ---
def cpumenuoptions():
    clearscn()
    print(" ")
    print(" ")
    
    settopmargins(False)
    # 🌟 Galti yahan theek ki gayi hai. Ab yeh function mil jayega.
    setcpuscreenmenus() 
    setbottommargins(False) 

    print("Enter any one of the above available options")
    
    try:
        cpumemoption=int(input())
    except ValueError:
        print("you have entered wrong option....")
        waitforesckey()
        clearscn()
        cpumenuoptions()
        return

    # Option 1: CPU Times
    if cpumemoption==1:
        clearscn()
        print(" ")
        print("CPU Times: ----")
        print(" ")
        print("***********************************************************************")
        cputimes()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        cpumenuoptions()
    
    # Option 2: System Memory
    elif cpumemoption==2:
        clearscn()
        print(" ")
        print("System Memory (RAM) Information: ----")
        print(" ")
        print("***********************************************************************")
        sysmemory()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        cpumenuoptions()

    # Option 3: CPU Utilization
    elif cpumemoption==3:
        clearscn()
        print(" ")
        print("Current CPU Utilization Percentage: ----")
        print(" ")
        print("***********************************************************************")
        cpu_utilization()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        cpumenuoptions()
        
    # Option 4: CPU Core/Thread Count
    elif cpumemoption==4:
        clearscn()
        print(" ")
        print("CPU Core/Thread Count: ----")
        print(" ")
        print("***********************************************************************")
        cpu_count_info()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        cpumenuoptions()
        
    # Option 5: Logged-in Users
    elif cpumemoption==5:
        clearscn()
        print(" ")
        print("Logged-in Users: ----")
        print(" ")
        print("***********************************************************************")
        logged_in_users()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        cpumenuoptions()
    
    # Option 6: Boot Time and Uptime
    elif cpumemoption==6:
        clearscn()
        print(" ")
        print("System Boot Time and Uptime: ----")
        print(" ")
        print("***********************************************************************")
        system_boot_time_and_uptime()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        cpumenuoptions()
        
    elif cpumemoption==100:
        clearscn()
        return 
    else:
        print("you have entered wrong option....")
        clearscn()
        cpumenuoptions()