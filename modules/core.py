import re
import subprocess
import psutil

# Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
def get_hostname():
    return subprocess.check_output("hostname", shell=True).decode('UTF-8').strip()

def get_local_ip():
    return subprocess.check_output("hostname -I | cut -d\' \' -f1", shell=True).decode('UTF-8').strip()

def get_cpu_temperature():
    temperature = subprocess.check_output("vcgencmd measure_temp", shell=True)
    return re.search('temp=(\d+)', temperature.decode('UTF-8')).group(1)

def get_cpu_useage():
    return "{:2.0f}".format(psutil.cpu_percent())

def get_memory_useage():
    return "{:2.0f}".format(psutil.virtual_memory().percent)

def get_usage_page(screen):
    screen.draw_text((0, 0), "NAME: " + get_hostname())
    screen.draw_text((0, 0 + 10), "IP  : " + get_local_ip())
    screen.draw_text((0, 0 + 20), "CPU : " + get_cpu_useage() + "% | MEM: " + get_memory_useage() + "%")

def get_temperature_page(screen):
    screen.draw_text((0, 0), "NAME: " + get_hostname())
    screen.draw_text((0, 0 + 10), "IP: " + get_local_ip())
    screen.draw_text((0, 0 + 20), "CPU: " + get_cpu_temperature() + "ºC | MEM: " + get_memory_useage() + "%")