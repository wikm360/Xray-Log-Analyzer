import schedule
from pytz import timezone
import time
import os
from detail import path_log ,  token , chat_id
import psutil
import requests

CPU_THRESHOLD = 50
RAM_THRESHOLD = 50

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)  # Get CPU usage over 1 second interval

def get_ram_usage():
    mem = psutil.virtual_memory()
    return mem.percent  # Get RAM usage percentage

def clear_def () : 
    with open(path_log , "w") :
        pass

def send_telegram_message(message):
    requests.get("https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + message)
def main() :
    schedule.every().day.at("23:00" , timezone("Asia/Tehran")).do(clear_def)
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