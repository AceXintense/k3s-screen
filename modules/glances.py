import requests

url = 'http://192.168.1.126:61208/api/3'

def get_cpu(element):
    return requests.get(url + '/cpu').json()[element]

def get_cpu_load(element):
    return requests.get(url + '/load').json()[element]

def get_swap_memory(element):
    return requests.get(url + '/memswap').json()[element]

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

def get_cpu_page(screen):
    screen.draw_text((0, 0), "TOTAL CPU: " + str(get_cpu('total')) + "%")
    screen.draw_text((0, 0 + 10), "IO WAIT: " + str(get_cpu('iowait')))
    screen.draw_text((0, 0 + 20), "I: " + str(get_cpu('idle')) + "% | U: " + str(get_cpu('user')) + "%")

def get_swap_memory_page(screen):
    screen.draw_text((0, 0), "TOTAL SWAP: " + sizeof_fmt(get_swap_memory('total')))
    screen.draw_text((0, 0 + 10), "SWAP PERCENT: " + str(get_swap_memory('percent')) + "%")
    screen.draw_text((0, 0 + 20), "F:" + sizeof_fmt(get_swap_memory('free')) + " | U:" + sizeof_fmt(get_swap_memory('used')))

def get_cpu_load_page(screen):
    screen.draw_text((0, 0), "1 MIN: " + str(get_cpu_load('min1')) + "%")
    screen.draw_text((0, 10), "5 MIN: " + str(get_cpu_load('min5')) + "%")
    screen.draw_text((0, 20), "15 MIN: " + str(get_cpu_load('min15')) + "%")