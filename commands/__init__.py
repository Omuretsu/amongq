import json
import os

CONFIG_FILE = "config.json"

# デフォルト値
DEFAULT_CAPACITY = 13

# config.json が存在すれば読み込む
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        DEFAULT_CAPACITY = data.get("default_capacity", DEFAULT_CAPACITY)

# 共通関数


def room_exists(bot, room_id: str) -> bool:
    return room_id in bot.room_data


def get_room(bot, room_id: str):
    return bot.room_data.get(room_id)


def save_default_capacity(capacity: int):
    global DEFAULT_CAPACITY
    DEFAULT_CAPACITY = capacity
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"default_capacity": DEFAULT_CAPACITY},
                  f, ensure_ascii=False, indent=2)
