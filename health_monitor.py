#!/usr/bin/env python3
"""
Cloud Resource Health Monitor
Monitors CPU, memory, disk usage, and uptime using only built-in libraries.
Designed for Linux systems.
"""

import json
import os
import shutil
import time


def get_cpu_usage():
    """Calculate CPU usage as a percentage."""
    try:
        # First reading
        with open('/proc/stat', 'r') as f:
            line1 = f.readline()
        parts1 = line1.split()
        times1 = [int(x) for x in parts1[1:]]

        # Wait for a short interval
        time.sleep(0.1)

        # Second reading
        with open('/proc/stat', 'r') as f:
            line2 = f.readline()
        parts2 = line2.split()
        times2 = [int(x) for x in parts2[1:]]

        # Calculate the total time spent in each mode between the two readings
        total_time1 = sum(times1)
        total_time2 = sum(times2)

        # The idle time is the 4th value (index 3) in the times list (user, nice, system, idle, ...)
        idle_time1 = times1[3]
        idle_time2 = times2[3]

        # Total time elapsed
        total_time_elapsed = total_time2 - total_time1
        # Time spent idle
        idle_time_elapsed = idle_time2 - idle_time1

        # CPU usage percentage
        if total_time_elapsed == 0:
            cpu_usage = 0.0
        else:
            cpu_usage = (1.0 - (idle_time_elapsed / total_time_elapsed)) * 100.0

        return round(cpu_usage, 2)
    except Exception as e:
        return f"Error reading CPU usage: {str(e)}"


def get_memory_usage():
    """Get memory usage from /proc/meminfo."""
    try:
        mem_info = {}
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 2:
                    key = parts[0].rstrip(':')
                    value = int(parts[1])
                    mem_info[key] = value  # in kB

        total = mem_info.get('MemTotal', 0)
        free = mem_info.get('MemFree', 0)
        buffers = mem_info.get('Buffers', 0)
        cached = mem_info.get('Cached', 0)
        # Calculate used memory
        used = total - (free + buffers + cached)
        usage_percent = (used / total) * 100.0 if total > 0 else 0.0
        return {
            'total': total,
            'used': used,
            'free': free,
            'buffers': buffers,
            'cached': cached,
            'usage_percent': round(usage_percent, 2)
        }
    except Exception as e:
        return {'error': str(e)}


def get_disk_usage():
    """Get disk usage for the root partition."""
    try:
        total, used, free = shutil.disk_usage('/')
        usage_percent = (used / total) * 100.0
        return {
            'total': total,
            'used': used,
            'free': free,
            'usage_percent': round(usage_percent, 2)
        }
    except Exception as e:
        return {'error': str(e)}


def get_uptime():
    """Get system uptime in seconds from /proc/uptime."""
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
        return round(uptime_seconds, 2)
    except Exception as e:
        return f"Error reading uptime: {str(e)}"


def main():
    """Main function to collect and output metrics as JSON in a loop."""
    interval = int(os.environ.get('MONITOR_INTERVAL', 10))
    while True:
        data = {
            'cpu_usage_percent': get_cpu_usage(),
            'memory_usage': get_memory_usage(),
            'disk_usage': get_disk_usage(),
            'uptime_seconds': get_uptime(),
            'timestamp': time.time()
        }
        print(json.dumps(data))
        # Flush to ensure output is sent immediately
        import sys
        sys.stdout.flush()
        time.sleep(interval)


if __name__ == '__main__':
    main()