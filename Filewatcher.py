import os
import time
import threading
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
#from win10toast import ToastNotifier
from winotify import Notification, audio
import pystray
from PIL import Image, ImageDraw
from pathlib import Path
from datetime import datetime


#pip install watchdog plyer pystray pillow
#pip install win10toast
#pip install winotify
#List multiple directories here
#WATCH_PATHS = [
#    r"D:\Watcher",
#]
#icon = None
#watcher = None
#LOG_FILE = os.path.join("D:\Vaidehi\Graduation\Graphic Era\Bhimtal\3rd Year\5th Sem\MidPBL", "directory_watcher_log.txt")
#LOG_FILE = Path(r"D:\Vaidehi\Graduation\Graphic Era\Bhimtal\3rd Year\5th Sem\MidPBL\directory_watcher_log.txt")

def load_config(config_path="config.json"):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    watch_paths = config.get("watch_paths", [])
    log_file = Path(config.get("log_file", "directory_watcher_log.txt"))
    icon_path = config.get("icon_path", None)

    return watch_paths, log_file, icon_path


WATCH_PATHS, LOG_FILE, ICON_PATH = load_config()

icon = None
watcher = None


def notify(title, message):
                    toast = Notification(
                    app_id="Directory Watcher",
                    title=title,
                    msg=message,
                    icon=ICON_PATH
                    )
                    toast.set_audio(audio.Default, loop=False)
                    toast.show()
                    
#toaster = ToastNotifier()
# -------Watcher Classes --------
class WatchHandler(FileSystemEventHandler):
    def __init__(self, log_func):
        super().__init__()
        self.log_func = log_func
    
    def on_any_event(self, event):
        # Only handle relevant event types
        if event.event_type not in ("created", "deleted", "moved"):
            return

        # Figure out what was affected
        name = os.path.basename(event.src_path)
        path = os.path.dirname(event.src_path)

        # Detect type: directory or file
        if event.is_directory:
            item_type = "Directory"
        else:
            # Even if deleted, try to infer from path
            item_type = "Directory" if not os.path.splitext(name)[1] else "File"

        event_type = event.event_type.capitalize()
        message = f"{item_type} {event_type}: {name} in {path}"

        # Log and show notification
        self.log_func(message)
        print(f"[{time.strftime('%H:%M:%S')}] {message}")
        notify(f"{item_type} {event_type}", message)

            

class DirectoryWatcher:
    def __init__(self, paths, log_func):
        self.paths = paths
        self.observer = Observer()
        self.log_func = log_func

    def start(self):
        handler = WatchHandler(self.log_func)
        for path in self.paths:
            if os.path.exists(path):
                self.observer.schedule(handler, path, recursive=True)
                self.log_func(f"Started watching: {path}")
            else:
                self.log_func(f"Could not find Path: {path}")
        self.observer.start()

    def stop(self):
        try:
            self.observer.stop()
            self.observer.join(timeout=2)
            self.log_func("Watcher stopped.")
        except Exception as e:
            self.log_func(f"Error stopping watcher: {e}")

# ------Logging -------
def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)


# ----- Tray Icon -------
def create_tray_icon(w):
    global watcher, icon
    watcher = w
    
    # Create a blue circular icon
    img = Image.new("RGB", (64, 64), color=(0, 102, 204))
    draw = ImageDraw.Draw(img)
    draw.ellipse((16, 16, 48, 48), fill=(255, 255, 255))

    #def on_quit(icon, item):
    #    log_event("Tray icon closing by user.")
    #    watcher.stop()
    #    icon.visible = False   # hide first
    #    time.sleep(0.5)        # give Windows a moment
    #    icon.stop()
    #    log_event("Tray icon closed by user.")

    icon = pystray.Icon(
        "Directory Watcher",
        icon=img,
        title="Directory Watcher",
        menu=pystray.Menu(
            pystray.MenuItem("Quit", on_quit)
        )
    )
    return icon
    
def on_quit(icon_obj=None, item=None):
    """stop the watcher and tray icon."""
    global icon, watcher
    try:
        if watcher:
            watcher.stop()
        if icon:
            icon.visible = False
            time.sleep(0.5)
            icon.stop()
        log_event("Tray icon closed via on_quit() call.")
        print("[INFO] Watcher and tray icon stopped.")
    except Exception as e:
        log_event(f"Error during on_quit(): {e}")
        print(f"[ERROR] on_quit(): {e}")

# ---------- Main Runner ----------
def run_watcher():
    log_event("run_watcher() running in thread: {threading.current_thread().name}")
    watcher = DirectoryWatcher(WATCH_PATHS, log_event)
    watcher_thread = threading.Thread(target=watcher.start, daemon=True)
    watcher_thread.start()
    log_event("Watcher running in background thread.")
    log_event("Watcher started in thread: {watcher_thread.name}")
    #print(f"Watcher started in thread: {watcher_thread.name}")

    icon = create_tray_icon(watcher)
    try:
        icon.run()  # Run tray in main thread
        log_event("Icon started in main thread.")
    except Exception as e:
        log_event(f"Tray icon error: {e}")
    finally:
        watcher.stop()


if __name__ == "__main__":
    run_watcher() 
    print("Active threads:", [t.name for t in threading.enumerate()])    
    
