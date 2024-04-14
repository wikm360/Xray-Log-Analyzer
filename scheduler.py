import schedule
from pytz import timezone
import time
import os
from detail import path_log

def clear_def () : 
    with open(path_log , "w") :
        pass
def main() :
    schedule.every().day.at("00:00" , timezone("Asia/Tehran")).do(clear_def)
    while True :
        schedule.run_pending()
        time.sleep(1)


main()