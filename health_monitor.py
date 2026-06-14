#!/usr/bin/env python3
"""
Cloud Resource Health Monitor
Monitors CPU, memory, disk usage, and uptime using only built-in libraries.
Designed for Linux systems.
"""

import json
import os
import shutil
import sys
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


def format_bytes_to_human_readable(bytes_num):
    """Convert bytes to human readable format (e.g., 1024 -> 1 KB)."""
    if bytes_num == 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while bytes_num >= 1024 and i < len(units) - 1:
        bytes_num /= 1024.0
        i += 1
    if i == 0:
        return f"{int(bytes_num)} {units[i]}"
    else:
        return f"{bytes_num:.2f} {units[i]}"


def format_uptime(seconds):
    """Format uptime seconds into hours and minutes."""
    if isinstance(seconds, str):
        return seconds  # error message
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    return f"{hours} hours, {minutes} minutes"


def format_timestamp(timestamp):
    """Format Unix timestamp to readable string."""
    t = time.localtime(timestamp)
    day = str(t.tm_mday)
    month = time.strftime("%b", t)
    year = str(t.tm_year)
    time_str = time.strftime("%H:%M:%S", t)
    return f"{day} {month} {year}, {time_str}"


def main():
    """Main function to collect and output metrics."""
    interval = int(os.environ.get('MONITOR_INTERVAL', 10))

    # Check if stdout is a terminal (for interactive formatted output)
    if sys.stdout.isatty():
        # Interactive mode: display formatted output
        while True:
            # Clear screen (ANSI escape)
            print("\033[H\033[J", end="")

            # Get metrics
            cpu_usage = get_cpu_usage()
            memory = get_memory_usage()
            disk = get_disk_usage()
            uptime_seconds = get_uptime()
            timestamp = time.time()

            # Format CPU usage (integer for display)
            if isinstance(cpu_usage, (int, float)):
                cpu_display = f"{int(round(cpu_usage))}%"
            else:
                cpu_display = cpu_usage  # error message

            # Format memory usage
            if isinstance(memory, dict) and 'error' not in memory:
                mem_used = memory['used'] * 1024  # convert kB to bytes
                mem_total = memory['total'] * 1024
                mem_percent = memory['usage_percent']
                mem_used_str = format_bytes_to_human_readable(mem_used)
                mem_total_str = format_bytes_to_human_readable(mem_total)
                mem_display = f"{mem_percent:.2f}%  ({mem_used_str} / {mem_total_str})"
            else:
                mem_display = memory.get('error', 'Unknown error') if isinstance(memory, dict) else memory

            # Format disk usage
            if isinstance(disk, dict) and 'error' not in disk:
                disk_used = disk['used']
                disk_total = disk['total']
                disk_percent = disk['usage_percent']
                disk_used_str = format_bytes_to_human_readable(disk_used)
                disk_total_str = format_bytes_to_human_readable(disk_total)
                disk_display = f"{disk_percent:.2f}%  ({disk_used_str} / {disk_total_str})"
            else:
                disk_display = disk.get('error', 'Unknown error') if isinstance(disk, dict) else disk

            # Format uptime
            uptime_display = format_uptime(uptime_seconds)

            # Format timestamp
            timestamp_display = format_timestamp(timestamp)

            # Print the boxed output
            print("╔══════════════════════════════════════╗")
            print("║       CLOUD RESOURCE MONITOR        ║")
            print("╚══════════════════════════════════════╝")
            print(f"CPU Usage       :  {cpu_display:>8}")
            print(f"Memory Usage    :  {mem_display:>8}")
            print(f"Disk Usage      :  {disk_display:>8}")
            print(f"Uptime          :  {uptime_display:>8}")
            print(f"Last Updated    :  {timestamp_display:>8}")
            print("")
            print("Refreshes every 10 seconds. Press Ctrl+C to stop.")

            # Flush to ensure output is sent immediately
            sys.stdout.flush()
            time.sleep(interval)
    else:
        # Non-interactive mode: output JSON (for Docker, logs, etc.)
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
            sys.stdout.flush()
            time.sleep(interval)


if __name__ == '__main__':
    main()