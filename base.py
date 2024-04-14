from detail import path_log , path_user
import os
import re

user_list = ["default"]

def delete_file (user):
        file_path = f"{path_user}{user}.txt"
        # Check if the file exists before attempting to delete it
        if os.path.exists(file_path):
            # Delete the file
            os.remove(file_path)
            print("File deleted successfully.")
        else:
            print("The file does not exist.")

with open (path_log , "r") as file :
    for line in file :
        pattern = r"email: (\S+)"
        user = re.findall(pattern, line)[0]
        user = user.split(".")[1].split("\n")[0]
        line = line.split(" ")
        if line[2] == "DNS" : 
            continue
        if user not in user_list :
            user_list.append(user)
        if user not in user_list : 
            with open (f"{path_user}{user}.txt"  , "w") as user_log :
                user_log.writelines(line)
        else  :
            with open (f"{path_user}{user}.txt"  , "a") as user_log :
                user_log.writelines(line)
        ##در ادامه بعد از ارسال فایل های دسته بندی شده در تلگرام باید حتما پاک بشن
        delete_file(user)
        
        
        
    print(user_list)


    