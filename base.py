from detail import path_log , path_user
import os
import re
import json

user_list = {"default":"0"}
line_str  =  " "
before_ip = "0.0.0.0"
before_port = "0"

def delete_file (user):
        file_path = f"{path_user}{user}.txt"
        # Check if the file exists before attempting to delete it
        if os.path.exists(file_path):
            # Delete the file
            os.remove(file_path)
            print("File deleted successfully.")
        else:
            print("The file does not exist.")
count = 0
with open (path_log , "r") as file :
    for line in file :
        pattern = r"email: (\S+)"
        #if user in line :
        if re.findall(pattern, line) :
            user = re.findall(pattern, line)[0]
            user = user.split(".")[1].split("\n")[0]
            line = line.split(" ")
            if line[2] == "DNS" : 
                continue
            if user not in user_list :
                user_list[user]  = 0
            if user not in user_list : 
                with open (f"{path_user}{user}.txt"  , "w") as user_log :
                    user_log.writelines(line)
            else  :
                with open (f"{path_user}{user}.txt"  , "a") as user_log :
                    user_log.writelines(line)
            user_list[user] = line[0] + " " +  line[1]
            count += 1

            #print(count)

            for pice in line :
                line_str += " " + pice
            
            #porn detection :
            pattern_porn = r"\b\w*\s*porn\s*\w*\b"
            if re.findall(pattern_porn, line_str):
                with open (f"{path_user}porn_detection.txt" , "a" , encoding="utf-8") as file : 
                    file.writelines(line_str)
            
            # port scan detection : 
            ip_port = line[2]
            ip = ip_port.split(":")[0]
            port = ip_port.split(":")[1]
            if ip == before_ip :
                if port != before_port : 
                    file_path = f"{path_user}port_scan_detection.txt"
                    with open(file_path , "a") as file : 
                        file.writelines(line_str)


            ##در ادامه بعد از ارسال فایل های دسته بندی شده در تلگرام باید حتما پاک بشن
            delete_file(user)
            line_str = " "
        
        
        
    file_path = f"{path_user}last_online_per_user.txt"
    json_data = json.dumps(user_list)
    with open (file_path , "w") as file : 
        file.writelines(json_data)
    print(user_list)


    