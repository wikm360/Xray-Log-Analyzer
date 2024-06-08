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
type_of_get_usage = "api_marzban" # "mysql" or "api_marzban" 
# database variable :
user_sql="root"
password="1234567890"
host="127.0.0.1"
database = "marzban"
# marzban API variable :
marzban_panel_url = " " # Example = "sub.panel.com:2096"
panel_username = "admin" # Example = admin
panel_pass = "1234567890" # Example = admin
# DNS URL for ignore :
ignore_urls = ["1.1.1.1"  , "mtalk.google.com" , "android.apis.google.com" , "dns.google" , "8.8.8.8" , "gstatic" , "10.10." , "1.0.0.1" , "8.8.4.4" , "cloudflare"]
############################################################
# Dont change These :
path_log = f"{path}access.log"
path_user = f"{path}user/"
