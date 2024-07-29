from detail import path_log , path_user , path  , token , chat_id  , origin_path_log ,  cpu_threshold , ram_threshold  , user_sql , password , host , database , type_of_get_usage ,  marzban_panel_url , ignore_urls , panel_username , panel_pass
import os
import re
import json
import schedule
from pytz import timezone
import time
import requests
import shutil
import psutil
from collections import Counter
import mysql.connector
import urllib.parse
from datetime import datetime , timedelta
from collections import defaultdict

CPU_THRESHOLD = cpu_threshold
RAM_THRESHOLD = ram_threshold

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)  # Get CPU usage over 1 second interval

def get_ram_usage():
    mem = psutil.virtual_memory()
    return mem.percent  # Get RAM usage percentage

def clear_originfile_def () : 
    with open(origin_path_log , "w") :
        pass
    analize()

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
    clear_originfile_def()

def send_telegram_message(message):
    requests.get("https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + message)

def delete_file (file_path):
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except OSError as e:
            print(f"Error deleting {file_path}: {e}")
    else:
        print(f"File '{file_path}' not found in '{file_path}'.")

def send_single_file (file_path) :
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    files = {'document': open(file_path, 'rb')}
    data = {'chat_id': chat_id}
    response = requests.get(url, files=files, data=data)
    if response.status_code == 200:
        print("File sent successfully.")
    else:
        print(f"Failed to send file. Status code: {response.status_code}")
        print(response.text)

def analize () :
    user_usage  =  {"default" : "0"}
    url_user_list = ["default"]
    user_list = {"default":"0"}
    user_phone =  {"default" : ["0"  , "1"]}
    inbound_user  = ["default"]
    p_user = ["default"]
    line_str  =  " "
    before_ip = "0.0.0.0"
    before_port = "0"
    count = 0
    with open (path_log , "r") as file :
        for line in file :
            count += 1
            pattern = r"email: (\S+)"
            #if user in line :
            if re.findall(pattern, line) :
                flag = True
                for li in ignore_urls :
                    if flag :
                        if li in line :
                            flag = False
                if flag :
                    user = re.findall(pattern, line)[0]
                    user = user.split(".")[1].split("\n")[0]
                    line = line.split(" ")

                    for pice in line :
                        line_str += " " + pice
                    
                    if line[2] == "DNS" : 
                        continue
                    if user not in user_list :
                        user_list[user]  = 0
                    if user not in user_list : 
                        with open (f"{path_user}{user}.txt"  , "w") as user_log :
                            user_log.writelines(line_str)
                    else  :
                        with open (f"{path_user}{user}.txt"  , "a") as user_log :
                            user_log.writelines(line_str)
                    user_list[user] = line[0] + " " +  line[1]
                    
                    #create url list request per user:
                    if "[" in  line[4] :
                        url = line[4].split("[")[1].split("]")[0]
                    else :
                        url = str(line[4].split(":")[1])
                    #print(url)
                    if user not in url_user_list : 
                        url_user_list.append(user)
                        with open (f"{path_user}{user}_url.txt"  , "w") as file :
                            file.writelines("default")

                    else  :
                        with open (f"{path_user}{user}_url.txt"  , "r") as file :
                            with open (f"{path_user}{user}_url.txt"  , "a") as file_2 :
                                for line_url in file :
                                    if url in line_url :
                                        flag  = True
                                    else :
                                        flag = False
                                if flag == False:
                                    file_2.writelines("\n")
                                    file_2.writelines(url)

                    
                    #porn detection :
                    pattern_porn = r"\b\w*\s*(porn|xnxx|xvideos|sex|brazzer|xxx|erotica|hardcore|BDSM|fetish|Nude|NSFW|PNP|CYOC|OnlyFans|camgirl|webcam)\s*\w*\b"
                    if re.findall(pattern_porn, line_str):
                        with open (f"{path}porn_detection.txt" , "a" , encoding="utf-8") as file : 
                            file.writelines(line_str)
                        if user not in p_user :
                            p_user.append(user)
                        
                    # phone detection : 
                    pattern = r"\b\w*\s*(xiaomi|samsung|dbankcloud)\s*\w*\b"
                    matches = re.findall(pattern, line_str)
                    if matches :
                        print(matches)
                        if user not in user_phone:
                            user_phone[user] = ["0"]
                        for match in matches:
                            if match in ["xiaomi", "samsung"] and match not in user_phone[f"{user}"]:
                                user_phone[user].append(match)
                            if match == "dbankcloud" and "huawei" not in user_phone[f"{user}"]:
                                user_phone[user].append("huawei")
                    
                    apple_pattern = r"\b\w*\s*gsp\s*\w*\b"
                    apple_pattern_2 = r"\b\w*\s*apple\s*\w*\b"
                    if re.findall(apple_pattern, line_str):
                        if re.findall(apple_pattern_2 , line_str) :
                            if user not in user_phone :
                                user_phone[f"{user}"] = ["0"]
                            if "apple" not in user_phone[f"{user}"] :
                                user_phone[f"{user}"].append("apple")
                    
                    # specific inbound detector  :
                    inbound_pattern = re.search(r"VMESS\s+\+\s+TCP", line_str, flags=re.IGNORECASE)
                    if inbound_pattern:
                        if user not in inbound_user :
                            inbound_user.append(user)
                    

                    line_str = " "
            
            print(count)
            
    file_path = f"{path}last_online_per_user.txt"
    json_data = json.dumps(user_list)
    p_data =  json.dumps(p_user)
    phone_data = json.dumps(user_phone)
    inbound_data = json.dumps(inbound_user)
    with open (file_path , "w") as file : 
        file.writelines(json_data)
    with open (f"{path}p_user.txt" , "w" , encoding="utf-8") as file :
        file.writelines(p_data)
    with open (f"{path}phone_user.txt" , "w" , encoding="utf-8") as file :
        file.writelines(phone_data)
    with open (f"{path}inbound_specific.txt" , "w" , encoding="utf-8") as file :
        file.writelines(inbound_data)

    #user usage : 

        #read old data from file :
    old_data = {}
    if os.path.isfile(f"{path}user_usage.txt"):
        with open (f"{path}user_usage.txt" , "r") as file : 
            old_data = json.load(file)

    user_usage  =  {"default" : "0"}

    if type_of_get_usage == "mysql" :
        db = mysql.connector.connect(user=user_sql, password=password,
                        host=host , database = database)
        cursor = db.cursor()
        for u in url_user_list : 
            if u != "default" :
                query = f"SELECT used_traffic FROM users where username = '{u}'"
                ## getting records from the table
                cursor.execute(query)
                ## fetching all records from the 'cursor' object
                records = cursor.fetchall()
                r = records[0][0]
                user_usage[u] = f"{r}"
                time.sleep(5)
        if db.is_connected():
            cursor.close()
            db.close()
            print("MySQL connection is closed")
    if type_of_get_usage == "api_marzban" :
        pass_Temp = urllib.parse.quote_plus(panel_pass)
        api_url = f"https://{marzban_panel_url}/api/admin/token"
        headers_dict = {"accept" : "application/json" , "Content-Type" : "application/x-www-form-urlencoded" }
        post_data = f"grant_type=&username={panel_username}&password={pass_Temp}&scope=&client_id=&client_secret="
        post_resault = requests.post(api_url , data=post_data , headers=headers_dict )
        data = json.loads(post_resault.text)
        Authorization_api = data["access_token"]
        pass_Temp = " "

        for u in url_user_list : 
            if u != "default" :
                url = f"https://{marzban_panel_url}/api/user/{u}/usage"
                dict = {"accept" : "application/json" , "Authorization" : f"Bearer {Authorization_api}"}
                resault = requests.get(url,headers=dict)
                data = json.loads(resault.text)
                usage = data["usages"][0]["used_traffic"]
                user_usage[u] = usage
                time.sleep(5)
    print(user_usage)
    #rewrite file :
    user_usage_json =  json.dumps(user_usage)
    with open (f"{path}user_usage.txt" , "w") as file :
        file.writelines(user_usage_json)

    #calculate diffrence and  create :
    if old_data :
        difference = {"default" : "0"}
        for n in url_user_list :
            if n != "default" :
                try :
                    new = int(user_usage[n]) - int(old_data[n])
                    difference[n] = new
                except :
                    pass
        print(difference)

        #calculate the max usage :
        if difference["default"] :
            del(difference["default"])
        max_usage  = max(difference.values())
        for name, usage in difference.items():
            if usage == max_usage:
                mess = f"The most usage person is {name} with {usage} ."
                send_telegram_message(mess)
    else :
        send_telegram_message("First time and no diffrence ....")


    print(user_list)

    #most used url per user : 
    print(url_user_list)
    for u in url_user_list :
        if u != "default" :
            with open(f"./user/{u}_url.txt", "r") as f:
            # Read the file content
                content = f.read()
            # Convert text to lowercase and split into urls
            urls = content.lower().split("\n")
            # Create a Counter object to count urls frequency
            url_count = Counter(urls)
            # Find the most common url and its count
            most_used_url, count = url_count.most_common(1)[0]
            # Print the most used url
            mess  = f"The most used URL is '{most_used_url}' (found {count} times) for {u}."
            print(mess)
            send_telegram_message(mess)

    #versatile person : 

    def parse_log_line(line):
        try :
            match = log_pattern.match(line)
            if match:
                date_str = match.group('date')
                time_str = match.group('time')
                datetime_str = f"{date_str} {time_str}"
                log_datetime = datetime.strptime(datetime_str, '%Y/%m/%d %H:%M:%S')
                
                domain = match.group('domain')
                # Check if the domain is a subdomain (has more than two parts)
                if domain.count('.') > 1:
                    return None
                
                return {
                    'datetime': log_datetime,
                    'source_ip': match.group('source_ip').strip('[]'),
                    'action': match.group('action'),
                    'domain': domain,
                    'user': match.group('user')
                }
        except :
            send_telegram_message("Error in parse log line ...")
        return None

    def analyze_versatile(log_lines):
        user_domain_requests = defaultdict(list)

        for line in log_lines:
            log_entry = parse_log_line(line)
            if log_entry:
                user_domain_key = (log_entry['user'], log_entry['domain'])
                user_domain_requests[user_domain_key].append(log_entry['datetime'])

        shortest_time_user = None
        shortest_time_domain = None
        max_requests = 0
        shortest_period = None

        for (user, domain), times in user_domain_requests.items():
            times.sort()
            if len(times) > 1:
                first_time = times[0]
                last_time = times[-1]
                period = last_time - first_time
                num_requests = len(times)

                if shortest_period is None or (period < shortest_period and num_requests > max_requests):
                    shortest_time_user = user
                    shortest_time_domain = domain
                    max_requests = num_requests
                    shortest_period = period

        return shortest_time_user, shortest_time_domain, max_requests, shortest_period
    try :
        log_pattern = re.compile(
        r'\s{2}(?P<date>\d{4}/\d{2}/\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) (tcp:|udp:)?(?P<source_ip>\[?[\da-fA-F:.]+\]?):\d+ (?P<action>\w+) '
        r'(tcp|udp):(?P<domain>[\w\.-]+):\d+ \[.*\] email: (?P<user>[\w\.@_]+)'
)
        with open(f"{path}porn_detection.txt", 'r') as f:
            log_lines = f.readlines()

        result = analyze_versatile(log_lines)
        if result:
            user, domain, requests, period = result
            mess = f"the most versatile person is {user} made the most requests ({requests}) to domain {domain} in the shortest period ({period})."
            send_telegram_message(mess)
        else:
            mess = "No sufficient data found in logs."
            send_telegram_message(mess)
    except :
        send_telegram_message("Erorr in detect versatile user...")

    # thirsty person : 
    def analyze_thirsty(log_lines):
        user_domain_requests = defaultdict(list)

        for line in log_lines:
            log_entry = parse_log_line(line)
            if log_entry:
                user_domain_key = (log_entry['user'], log_entry['domain'])
                user_domain_requests[user_domain_key].append(log_entry['datetime'])

        longest_time_user = None
        longest_time_domain = None
        longest_period = None

        for (user, domain), times in user_domain_requests.items():
            times.sort()
            if len(times) > 1:
                first_time = times[0]
                last_time = times[-1]
                period = last_time - first_time

                # Check if the period is less than or equal to 3 hours (timedelta in seconds)
                if period <= timedelta(hours=3):
                    # Check if this is the longest period found
                    if longest_period is None or period > longest_period:
                        longest_time_user = user
                        longest_time_domain = domain
                        longest_period = period
                else:
                    # If the period exceeds 3 hours, skip this user-domain pair
                    continue

        # If longest_time_user is still None, it means no valid entry was found within the time limit
        if longest_time_user is None:
            return None, None, None
        else:
            return longest_time_user, longest_time_domain, longest_period
    try :
        with open(f"{path}porn_detection.txt", 'r') as f:
            log_lines = f.readlines()

        result_user, result_domain, result_period = analyze_thirsty(log_lines)
        if result_user:
            mess = f"The most thirsty person is {result_user} spent the longest period ({result_period}) on main domain {result_domain}."
            send_telegram_message(mess)
        else:
            mess = "No sufficient data found or all users exceeded 3 hours on main domains."
            send_telegram_message(mess)
    except :
        send_telegram_message("Erorr in detect thirsty user ...")

    send_def()

def send_def () :
    source_dir = path_user
    output_filename = path + "user"
    # Ensure the source directory exists
    if not os.path.isdir(source_dir):
        raise ValueError(f"Source directory '{source_dir}' does not exist.")
    # Create the zip file
    shutil.make_archive(output_filename, 'zip', source_dir)

    send_file_list = ['./user.zip' , './inbound_specific.txt' , './last_online_per_user.txt' , './phone_user.txt' ,
                      './porn_detection.txt' , './user_usage.txt' ,'./p_user.txt' ,  path_log ]
    
    for file_path in send_file_list :
        try :
            send_single_file(file_path)
        except :
            pass
    
    time.sleep(15)

    clear_def()
  
def clear_def() :
    # هرچی توی پوشه یوزر هست پاک یشه
    for filename in os.listdir(path_user):
        file_path = os.path.join(path_user, filename)
        if os.path.isfile(file_path):  # Check if it's a file
            try:
                os.remove(file_path)
                print(f"Deleted file: {filename}")
            except OSError as e:
                print(f"Error deleting {filename}: {e}")
    
    # تک تک تکست های آنالیز پاک بشن
    clear_file_list = ["./inbound_specific.txt" , "./last_online_per_user.txt" , "./phone_user.txt" , "./porn_detection.txt" , "./p_user.txt" ,
                       "./access.log" ,"./user.zip" ]
    
    for f in clear_file_list :
        try :
            delete_file(f)
        except :
            pass
    
    send_telegram_message('''🇩​​🇴​​🇳​​🇪​ 
< ​🇨​​🇷​​🇪​​🇦​​🇹​​🇪​​🇩​ ​🇧​​🇾​ @wikm360 ​🇼​​🇮​​🇹​​🇭​ ❤️ > 
​🇻​3️⃣.5️⃣''')


def main() :
    #analize()
    schedule.every().day.at("04:00" , timezone("Asia/Tehran")).do(copy_def)
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