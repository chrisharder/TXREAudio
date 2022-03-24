#!/usr/bin/python
# L33t Tech -- MPC/MPD Audio Stream Watch Dog

from datetime import datetime
import subprocess
import json
import time
import requests
from sys import exit

def determine_difference(play_time, sys_uptime):
    # Here we will find if they are different. If they are +/-5 seconds off reboot.
    online_time = play_time.split(", ")
    system_time = sys_uptime.split(", ")
    
    raw_string_online = online_time[1]
    raw_string_system = system_time[1]
    
    online_time = online_time[1].split(":")
    system_time = system_time[1].split(":")
    
    # Convert and compare seconds
    o_seconds = online_time[2]
    s_seconds = system_time[2]
    print(o_seconds[0])
    
    # Compare seconds
    if (online_time[2][0] == "0"):
    	online_seconds = online_time[2][1]
    	bottom_online_seconds = int(online_seconds) - 15
    	top_online_seconds = int(online_seconds) + 15
    else:
    	online_seconds = online_time[2]
    	bottom_online_seconds = int(online_seconds) - 15
    	top_online_seconds = int(online_seconds) + 15
    
    if (system_time[2][0] == "0"):
    	system_seconds = system_time[2][1]
    else:
    	system_seconds = system_time[2]
    
    bottom_sys_seconds = int(system_seconds) - 15
    top_sys_seconds = int(system_seconds) + 15
    
    # Need to handle bottom and top of minutes now
    if (int(system_seconds) <= 15):
    	seconds_differential = 15 - int(system_seconds)
    	seconds_differential = 60 - seconds_differential
    	
    online = datetime.strptime(raw_string_online, "%H:%M:%S")
    system = datetime.strptime(raw_string_system, "%H:%M:%S")
    threshold = datetime.strptime("00:00:30", "%H:%M:%S")
    base = datetime.strptime("00:00:00", "%H:%M:%S")
    
    threshold_difference = threshold - base
    difference = system - online
    print(str(difference))
    print(str(threshold_difference))
    
    if (difference > threshold_difference):
    	print("Outage Indicated! Rebooting...")
    	command = "sudo reboot"
    	reboot_p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    	(raw_output, err_reboot) = p.communicate()
    

def get_mpc_stats():
    try:
        status = 10
	command = "mpc stats"
	p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	(raw_output, err_mpc) = p.communicate()
	raw_output = raw_output.split("Play Time:")
	raw_output2 = raw_output[1].split("Uptime:")
	output = raw_output2[1].split("DB Updated:")
	
	play_time = raw_output2[0].strip()
	play_time = play_time.replace("\n", "")
	
	sys_uptime = output[0].strip()
	sys_uptime = sys_uptime.replace("\n", "")
	
	print("Play Time: {0}".format(play_time))
	print("System Uptime: {0}".format(sys_uptime))
	
	determine_difference(play_time, sys_uptime)
		
    except Exception as e:
        print(e)
    
    return status

def main():
# This will be cron jobbed. Repped once a minute.
# Need to get status of mpc-based stream.
#  status = get_mpc_status()
    command = "mpc play"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (raw_output, err_mpc) = p.communicate()
    print(raw_output)
    time.sleep(10)
    status = get_mpc_stats()
  
if __name__ == "__main__":
    print("Starting Program...")
    main()
  
  
