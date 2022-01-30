import re
import subprocess
import modules.core

def describe_node():
    cmd = "kubectl describe node " + modules.core.get_hostname()
    return subprocess.check_output(cmd, shell=True).decode('UTF-8')

def get_pods():
    return re.search('(\d) in ', describe_node()).group(1)

def get_page(screen):
    pods = get_pods()
    screen.drawText((0, 0), "NAME: " + modules.core.get_hostname())
    screen.drawText((0, 10), "IP: " + modules.core.get_local_ip())
    screen.drawText((0, 20), "PODS: " + pods + " | TEMP: " + modules.core.get_cpu_temperature() + "c")