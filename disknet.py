# disknet.py (Final Corrected Code with Active Network Connections)

from util import * 
import psutil
from chart import *

# --- Helper function to convert bytes to human-readable format ---
def convert_bytes(bytes_num):
    """Converts bytes to KB, MB, GB, or TB."""
    if bytes_num is None:
        return 'N/A'
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    for unit in units:
        if bytes_num < 1024.0:
            return f"{bytes_num:.2f} {unit}"
        bytes_num /= 1024.0
    return f"{bytes_num:.2f} PB"

# --- Option 1: Disk partitions (Renamed function for clarity, but keeping original logic) ---
def diskusage():
    parlist = psutil.disk_partitions()
    i = 0
    print("Total number of partitions: " + str(len(parlist)))
    print("")
    
    # Headers
    print(f"{'Mountpoint':<25}{'Device':<25}{'FSType':<10}")
    print("-" * 60)
    
    for part in parlist:
        i += 1
        # Print main partition info
        print(f"{part.mountpoint:<25}{part.device:<25}{part.fstype:<10}")
        # Detailed info (Original code ki tarah)
        print("-------Partition " + str(i) + "--------------")
        for key, value in part._asdict().items():
            print(f"{key}:    {value}")
        print("--------------------------------")


# --- Option 2: Disk I/O statistics ---
def disk_io_stats():
    disk_io = psutil.disk_io_counters()
    if not disk_io:
        print("Disk I/O statistics not available.")
        return
        
    print("--- Disk I/O Counters (All Disks) ---")
    print(f"Read Count:           {disk_io.read_count:,}")
    print(f"Write Count:          {disk_io.write_count:,}")
    print(f"Read Bytes:           {convert_bytes(disk_io.read_bytes)}")
    print(f"Write Bytes:          {convert_bytes(disk_io.write_bytes)}")
    print(f"Read Time (ms):       {disk_io.read_time:,}")
    print(f"Write Time (ms):      {disk_io.write_time:,}")

# --- Option 3: Disk usage ---
def get_disk_usage():
    print(f"{'Mountpoint':<25}{'Total':<15}{'Used':<15}{'Free':<15}{'Used %':<10}")
    print("-" * 80)
    labels = ['Used', 'Free']
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
               
            print(f"{partition.mountpoint:<25}"
                  f"{convert_bytes(usage.total):<15}"
                  f"{convert_bytes(usage.used):<15}"
                  f"{convert_bytes(usage.free):<15}"
                  f"{usage.percent:<10.1f}%")
            def get_sizes():
                return [usage.used, usage.free]
            getpiechart_live(get_sizes, labels, refresh_rate=2)
        except PermissionError:
            # Jaise /proc, /sys filesystems ko skip karne ke liye
            print(f"{partition.mountpoint:<25}{'(Permission Denied)':<60}")
 
 
# --- Option 4: Network I/O statistics ---
def network_io_stats():
    net_io = psutil.net_io_counters()
    if not net_io:
        print("Network I/O statistics not available.")
        return
    
    print("--- Network I/O Counters (All Interfaces) ---")
    print(f"Bytes Sent:         {convert_bytes(net_io.bytes_sent)}")
    print(f"Bytes Received:     {convert_bytes(net_io.bytes_recv)}")
    print(f"Packets Sent:       {net_io.packets_sent:,}")
    print(f"Packets Received:   {net_io.packets_recv:,}")
    print(f"Errors Incoming:    {net_io.errin:,}")
    print(f"Errors Outgoing:    {net_io.errout:,}")
    print(f"Drops Incoming:     {net_io.dropin:,}")
    print(f"Drops Outgoing:     {net_io.dropout:,}")


# --- Option 5: Active Network Connections (NEW FEATURE) ---
def get_active_connections():
    """Displays active network connections (sockets)."""
    
    # connections() call, TCP aur UDP sockets ko shamil karta hai
    connections = psutil.net_connections(kind='inet') 
    
    if not connections:
        print("No active INET connections found.")
        return

    # Headers
    print(f"{'PID':<6}{'Protocol':<10}{'Local Address':<30}{'Remote Address':<30}{'Status':<15}")
    print("-" * 91)
    
    # Top 20 connections hi dikhate hain, taaki screen overflow na ho
    count = 0
    for conn in connections:
        if count >= 20:
            print(f"... Showing top 20 connections. Total found: {len(connections)}.")
            break
            
        # Protocol ka naam (TCP/UDP)
        proto = "TCP" if conn.type == 1 else "UDP" if conn.type == 2 else "Other"
        
        # Local Address: IP:Port
        local_addr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else 'N/A'
        
        # Remote Address: IP:Port (Agar connection established hai)
        remote_addr = 'N/A'
        if conn.raddr:
            # Check karte hain ki Remote Address mein IP aur Port dono hain ya nahi
            if hasattr(conn.raddr, 'ip') and hasattr(conn.raddr, 'port'):
                 remote_addr = f"{conn.raddr.ip}:{conn.raddr.port}"
        
        # Status (e.g., ESTABLISHED, LISTEN, CLOSE_WAIT)
        status = conn.status if conn.status else 'N/A'
        
        # PID (Agar available hai)
        pid = conn.pid if conn.pid else 'N/A'
        
        print(f"{str(pid):<6}{proto:<10}{local_addr:<30}{remote_addr:<30}{status:<15}")
        count += 1

# --- Main Menu Handler (DiskNet Menu) ---

def disknetmenuoptions():
    settopmargins(True)
    # NOTE: setdiskscreenmenus() function ko util.py mein update karna hoga!
    setdiskscreenmenus() 
    setbottommargins(True)
    
    try:
        disknetoption = int(input())
    except ValueError:
        clearscn()
        print("Invalid input. Please enter a number.")
        disknetmenuoptions()
        return

    # Option 1: Disk partitions
    if disknetoption == 1:
        clearscn()
        print(" \nDisk partitions: ----\n ")
        print("***********************************************************************")
        diskusage() # Existing function for partitions
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        disknetmenuoptions()

    # Option 2: Disk I/O statistics
    elif disknetoption == 2:
        clearscn()
        print(" \nDisk I/O statistics: ----\n ")
        print("***********************************************************************")
        disk_io_stats()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        disknetmenuoptions()
        
    # Option 3: Disk usage
    elif disknetoption == 3:
        clearscn()
        print(" \nDisk usage: ----\n ")
        print("***********************************************************************")
        get_disk_usage()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        disknetmenuoptions()

    # Option 4: Network I/O statistics
    elif disknetoption == 4:
        clearscn()
        print(" \nNetwork I/O statistics: ----\n ")
        print("***********************************************************************")
        network_io_stats()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        disknetmenuoptions()
        
    # --- Option 5 Handler (NEW) ---
    elif disknetoption == 5:
        clearscn()
        print(" \nActive Network Connections (Top 20): ----\n ")
        print("***********************************************************************")
        get_active_connections() 
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        disknetmenuoptions()

    elif disknetoption == 100:
        clearscn()
        return 
    else:
        print("You have entered wrong option....")
        clearscn()
        disknetmenuoptions()