import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Log dosyasının yolu
LOG_FILE = "/home/ubuntu/bsm/logs/changes.json"
WATCH_DIRECTORY = "/home/ubuntu/bsm/test"

# Log dosyasını kontrol et ve oluştur
if not os.path.exists(os.path.dirname(LOG_FILE)):
    os.makedirs(os.path.dirname(LOG_FILE))
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as f:
        json.dump([], f)

class ChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        log_entry = {
            "event_type": event.event_type,
            "src_path": event.src_path,
            "is_directory": event.is_directory
        }
        self.log_change(log_entry)

    def log_change(self, log_entry):
        try:
            with open(LOG_FILE, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []

        data.append(log_entry)

        with open(LOG_FILE, 'w') as f:
            json.dump(data, f, indent=4)

def start_observer():
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_DIRECTORY, recursive=True)
    observer.start()
    print(f"Watching directory: {WATCH_DIRECTORY}")
    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    start_observer()

