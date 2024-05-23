import schedule
from pytz import timezone
import time
import os
from detail import path_log ,  token , chat_id
import psutil
import requests
import shutil
from detail import origin_path_log  , path_log

CPU_THRESHOLD = 50
RAM_THRESHOLD = 50

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)  # Get CPU usage over 1 second interval

def get_ram_usage():
    mem = psutil.virtual_memory()
    return mem.percent  # Get RAM usage percentage

def clear_originfile_def () : 
    with open(origin_path_log , "w") :
        pass

def copy_def () :
    source_path = origin_path_log
    destination_path = path_log
    try:
        shutil.copy2(source_path, destination_path)
        print(f"File '{source_path}' copied successfully to '{destination_path}'.")
    except FileNotFoundError:
        print(f"Error: File '{source_path}' not found.")
    except PermissionError:
        print(f"Error: Insufficient permission to copy the file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def send_telegram_message(message):
    requests.get("https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + message)
def main() :
    schedule.every().day.at("23:00" , timezone("Asia/Tehran")).do(copy_def)
    schedule.every().day.at("23:15" , timezone("Asia/Tehran")).do(clear_originfile_def)
    while True :
        schedule.run_pending()
        cpu_usage = get_cpu_usage()
        ram_usage = get_ram_usage()

        if cpu_usage > CPU_THRESHOLD:
            message = f"CPU usage exceeded threshold: {cpu_usage}%"
            send_telegram_message(message)

        if ram_usage > RAM_THRESHOLD:
            message = f"RAM usage exceeded threshold: {ram_usage}%"
            send_telegram_message(message)
        time.sleep(1)


main()