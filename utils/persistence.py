import json
import os
from config import EVENTS_DIR

os.makedirs(EVENTS_DIR, exist_ok=True)

def save_event(event_id, data):
    file_path = os.path.join(EVENTS_DIR, f"{event_id}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_event(event_id):
    file_path = os.path.join(EVENTS_DIR, f"{event_id}.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def load_all_events():
    events = {}
    for fname in os.listdir(EVENTS_DIR):
        if fname.endswith(".json"):
            eid = fname[:-5]
            events[eid] = load_event(eid)
    return events

def list_events_by_date(date_str):
    files = [f for f in os.listdir(EVENTS_DIR) if f.startswith(date_str)]
    return files
