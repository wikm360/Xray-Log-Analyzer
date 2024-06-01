############################################################
# change this variable with your own :
path = "/home/wikmgg/Documents/GitHub/Xray-Log-Analyzer/"
#path = "/root/Xray-Log-Analyzer/"
origin_path_log = "/var/lib/marzban/log/access.log"
chat_id = "877591460"
# chat_id = '877591460'
token = "6386634380:AAGdHDGK3hmoo5vh2IRj3w0Ntgb47XAoZhQ"
# token = '6386634380:AAGdHDGK3hmoo5vh2IRj3w0Ntgb47XAoZhQ'
cpu_threshold = 75
ram_threshold = 80
#database variable :
user_sql="root"
password="1234567890"
host="127.0.0.1"
database = "marzban"
type_of_get_usage = "api_marzban" # "mysql" or "api_marzban" 
Authorization_api = " "  # Example = "Bearer ey###########"
marzban_pane_url = " " # Example = "sub.panel.com:2096"
ignore_urls = ["1.1.1.1"  , "mtalk.google.com" , "android.apis.google.com" , "dns.google" , "8.8.8.8" , "gstatic" , "10.10." , "1.0.0.1" , "8.8.4.4" , "cloudflare"]
############################################################

path_log = f"{path}access.log"
path_user = f"{path}user/"
