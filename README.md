
# Xray-Log-Analyzer

Created by wikm with ❤️

What does this bot do?
1) analyze the xray log every day and send to you with telegram bot
2) user phone detection
3) porn detection
4) classification users log per user 
5) specific inbound detection for users
6) clear old logs
7) CPU threshold alarm
8) RAM threshold alarm
9) ulr list per user
10) most ulr used per user
11) calculate and send The most used user 
12) send users usage ( get with mysql and marzban API )
13) send user who has the most request in shortest time (versatile person) (in porn sites)
14) send user who spend the longest period in one domain (thirsty person) (in porn sites)
15) detect suspicious Domains and IPs and report by telegram

more features coming 🔜

## Prerequisites

Before installing the required libraries, you must first install Python and pip

```bash
  pip install psutil
  pip install shutil
  pip install requests
  pip install time
  pip install pytz
  pip install schedule
  pip install json
  pip install re
  pip install os
  pip install collections
  pip install mysql-connector-python
  pip install DateTime
```
## Get

First, download and extract the project with the following command :

```bash
  wget https://github.com/wikm360/Xray-Log-Analyzer/releases/latest/download/Xray-Log-Analyzer.zip
  unzip Xray-Log-Analyzer.zip -d /root/Xray-Log-Analyzer
  cd Xray-Log-Analyzer/
```

## Change Variable 

```bash
  nano detail.py
```
change variables with your own ...

## Start Bot 

```bash
  sudo python3 base.py
```
