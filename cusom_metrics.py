#!/usr/bin/env python3
from prometheus_client import start_http_server, Gauge
import time, os, logging, psutil
from ping3 import ping

# Logging definition
logging.basicConfig(
  level=logging.INFO, format="%(levelname)s | %(asctime)s | %(message)s",
  datefmt='%Y-%m-%d %H:%M:%S',
)

# Define Prometheus gauge metric
PING_VALUE = Gauge('ping_rsponse_time', 'Time of ping', ['target'])
DISK_TOTAL = Gauge('node_disk_total_space', 'Ammount of disk space', ['device'])
DISK_USAGE = Gauge('node_disk_usage_space', 'Ammount of disk usage', ['device'])
MEMORY_TOTAL = Gauge('node_memory_total_amount', 'Ammount of memory')
MEMORY_USED = Gauge('node_memory_usage_amount', 'Ammount of memory used')
UPTIME = Gauge('uptime', 'Uptime')

# Ping Targets
hosts = (os.environ['PING_TARGETS']).split(',')

def ping_function(target:str) -> float:
  ping_time = ping(target, unit='s', timeout=10)
  return ping_time

# Disk metrics
types_monitor = (os.environ['DISK_TYPES_TO_MONITOR']).split(',')
def get_disk_info():
  disk_info = {}
  partitions = psutil.disk_partitions(all=False)
  for partition in partitions:
      for ptype in types_monitor:
        if ptype in partition.device:
          usage = psutil.disk_usage(partition.mountpoint)
          disk_info[partition.device] = {
              "mountpoint": partition.mountpoint,
              "total": usage.total,
              "used": usage.used,
              "free": usage.free,
              "percent": usage.percent
          }
  return disk_info

# Memory Metrics
def get_memory_info():
  memory_info = {}
  memory = psutil.virtual_memory()
  memory_info = {
    "total": memory.total,
    "used": memory.used
  }
  return memory_info

if __name__ == '__main__':
  # Start Prometheus HTTP server on port 8000
  start_http_server(8000)
  logging.info('======== Serving metrics at :8000; Metric are collected every 20s ========')

  while True:
    time.sleep(20)
    try:
      for target in hosts:
        ping_time = ping_function(target)
        PING_VALUE.labels(target).set(ping_time)
        logging.info('Sucessfull ping %s', target)
    except:
      logging.info('Unsucessfull ping %s', target)
    try:
      disk_info = get_disk_info()
      for device, info in disk_info.items():
        DISK_TOTAL.labels(device).set(info['total'])
        DISK_USAGE.labels(device).set(info['used'])
        logging.info('Sucessfull get disk data %s', device)
    except:
      logging.info('Unsucessfull getting disk data %s', device)
    try:
      memory_info = get_memory_info()
      MEMORY_TOTAL.set(memory_info['total'])
      MEMORY_USED.set(memory_info['used'])
      logging.info('Sucessfull get memory info')
    except:
      logging.info('Unsucessfull getting memory info')
    try:
      UPTIME.set(time.time() - psutil.boot_time())
    except:
      logging.info('Cannot get uptime')
