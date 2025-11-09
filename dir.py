import os
import threading
from Filewatcher import run_watcher, on_quit
from util import *
import shutil # File copy/move ke liye joda gaya hai

watcher_thread = None
# --- 1. Get Current Directory (Existing) ---
def getcurrentdir():
    cwd = os.getcwd() 
    print("Current working directory:", cwd)

# --- 2. Change Directory ---
def changedir():
    new_path = input("Enter the new directory path (Example: C:\\Users\\MyUser): ")
    try:
        os.chdir(new_path)
        print(f"\nSuccess: Directory successfully changed to:\n{os.getcwd()}")
    except FileNotFoundError:
        print(f"\nError: The path '{new_path}' was not found.")
    except NotADirectoryError:
        print(f"\nError: '{new_path}' is not a directory.")
    except PermissionError:
        print(f"\nError: Permission denied. Cannot change to '{new_path}'.")
    except Exception as e:
        print(f"\nUnexpected Error: {e}")

# --- 3. List Directory Content ---
def listdir():
    path = input("Enter the directory path to list (Press Enter for current directory): ")
    if not path:
        path = os.getcwd()
        
    print(f"\nListing contents of: {path}\n")
    try:
        contents = os.listdir(path)
        if not contents:
            print("(Directory is empty)")
            return
            
        print(f"{'Type':<10}{'Name':<50}")
        print("-" * 60)
        
        for item in contents:
            full_path = os.path.join(path, item)
            item_type = ""
            
            if os.path.isdir(full_path):
                item_type = "DIR"
            elif os.path.isfile(full_path):
                item_type = "FILE"
            else:
                item_type = "OTHER"
                
            print(f"{item_type:<10}{item:<50}")

    except FileNotFoundError:
        print(f"Error: Directory not found at '{path}'")
    except PermissionError:
        print(f"Error: Permission denied to access '{path}'.")
    except Exception as e:
        print(f"Unexpected Error: {e}")

# --- 4. Create a new directory (mkdir) ---
def createdir():
    new_dir_path = input("Enter the FULL path for the new directory: ").strip()
    if not new_dir_path:
        print("\nError: Path cannot be empty.")
        return
    try:
        os.makedirs(new_dir_path)
        print(f"\nSuccess: Directory created at '{new_dir_path}'")
    except FileExistsError:
        print(f"\nError: Directory already exists at '{new_dir_path}'.")
    except Exception as e:
        print(f"\nUnexpected Error while creating directory: {e}")

# --- 5. Remove an empty directory (rmdir) ---
def removedir():
    dir_to_remove = input("Enter the FULL path of the directory to remove (Must be EMPTY): ").strip()
    if not dir_to_remove:
        print("\nError: Path cannot be empty.")
        return
    try:
        os.rmdir(dir_to_remove)
        print(f"\nSuccess: Empty directory removed: '{dir_to_remove}'")
    except FileNotFoundError:
        print(f"\nError: Directory not found at '{dir_to_remove}'.")
    except OSError as e:
        if "Directory not empty" in str(e):
            print(f"\nError: Directory is NOT empty. Use recursive deletion (Rmdir -r option) if implemented.")
        else:
            print(f"\nUnexpected OSError: {e}")
    except Exception as e:
        print(f"\nUnexpected Error: {e}")

# --- 6. Copy a File ---
def copy_file():
    """Copies a file from a source path to a destination path."""
    source_path = input("Enter the FULL source file path (e.g., C:\\data\\file.txt): ").strip()
    destination_path = input("Enter the FULL destination path (folder or new filename): ").strip()

    if not os.path.exists(source_path):
        print(f"\nError: Source file not found at '{source_path}'")
        return

    try:
        shutil.copy(source_path, destination_path)
        print(f"\nSuccess: File successfully copied from:")
        print(f"Source: {source_path}")
        print(f"Dest:   {destination_path}")

    except PermissionError:
        print("\nError: Permission denied. Check file permissions or run as administrator.")
    except Exception as e:
        print(f"\nUnexpected Error during copy: {e}")

# --- 7. Move/Rename a File ---
def move_file():
    """Moves or renames a file using the shutil module."""
    source_path = input("Enter the FULL source file path (file to move/rename): ").strip()
    destination_path = input("Enter the FULL destination path (folder or NEW filename): ").strip()

    if not os.path.exists(source_path):
        print(f"\nError: Source file/folder not found at '{source_path}'")
        return

    try:
        shutil.move(source_path, destination_path)
        print(f"\nSuccess: File successfully moved/renamed from:")
        print(f"Source: {source_path}")
        print(f"Dest:   {destination_path}")

    except PermissionError:
        print("\nError: Permission denied. Check file permissions or run as administrator.")
    except Exception as e:
        print(f"\nUnexpected Error during move/rename: {e}")

# --- 8. Get Absolute Path of a File/Directory ---
def get_absolute_path():
    """Gets and displays the absolute path of a given file or directory."""
    relative_path = input("Enter the path or filename (relative or absolute) to get its full path: ").strip()

    if not relative_path:
        print("\nError: Path cannot be empty.")
        return

    try:
        absolute_path = os.path.abspath(relative_path)
        
        print("\nSuccess: Complete Source Path (Absolute Path) Found:")
        print(f"Path: {absolute_path}")
            
        if os.path.exists(absolute_path):
            print("Status: Path Exists on system.")
            if os.path.isdir(absolute_path):
                print(f"Type: Directory")
            elif os.path.isfile(absolute_path):
                print(f"Type: File")
        else:
            print("Status: Path does NOT exist on system.")
            print("Note: Yeh woh location hai jo system assume karta hai aapki current directory ke hisaab se.")
            
    except Exception as e:
        print(f"\nUnexpected Error: {e}")


# --- Main Menu Handler (Directory Menu) ---
def dirmenuoptions():
    global watcher_thread
    settopmargins(True)
    setdirscreenmenus()
    setbottommargins(True)
    if watcher_thread is None or not watcher_thread.is_alive():
        watcher_thread = threading.Thread(target=run_watcher, daemon=True, name="FileWatcherThread")
        watcher_thread.start()
    try:
        diroption = int(input())
    except ValueError:
        clearscn()
        print("Invalid input. Please enter a number.")
        dirmenuoptions()
        return

    if diroption == 1:
        clearscn()
        print(" \nCurrent working directory: ----\n ")
        print("***********************************************************************")
        getcurrentdir()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        dirmenuoptions()

    elif diroption == 2:
        clearscn()
        print(" \nChange directory (cd): ----\n ")
        print("***********************************************************************")
        changedir()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        dirmenuoptions()
        
    elif diroption == 3:
        clearscn()
        print(" \nList directory content: ----\n ")
        print("***********************************************************************")
        listdir()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        dirmenuoptions()
        
    elif diroption == 4:
        clearscn()
        print(" \nCreate a new directory (mkdir): ----\n ")
        print("***********************************************************************")
        createdir()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        dirmenuoptions()
        
    elif diroption == 5:
        clearscn()
        print(" \nRemove an empty directory (rmdir): ----\n ")
        print("***********************************************************************")
        removedir()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        dirmenuoptions()

    # --- Option 6 Handler ---
    elif diroption == 6:
        clearscn()
        print(" \nCopy a File (shutil.copy): ----\n ")
        print("***********************************************************************")
        copy_file()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        dirmenuoptions()

    # --- Option 7 Handler ---
    elif diroption == 7:
        clearscn()
        print(" \nMove or Rename a File (shutil.move): ----\n ")
        print("***********************************************************************")
        move_file()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        dirmenuoptions()


    # --- Option 8 Handler ---
    elif diroption == 8:
        clearscn()
        print(" \nFind Complete Source Path (Absolute Path): ----\n ")
        print("***********************************************************************")
        get_absolute_path()
        print("***********************************************************************")
        waitforesckey()
        clearscn()
        dirmenuoptions()


    elif diroption == 100:
        on_quit()
        clearscn()
        return 
    else:
        print("you have entered wrong option....")
        clearscn()
        dirmenuoptions()