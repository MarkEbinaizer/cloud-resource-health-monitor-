# Cloud Resource Health Monitor

A simple tool that shows your computer's CPU, memory, disk usage and uptime in an easy-to-read format.

## What This Does

This app continuously monitors your system's vital signs:
- **CPU Usage** – how hard your processor is working
- **Memory Usage** – how much RAM is being used
- **Disk Usage** – how much storage space is taken up
- **Uptime** – how long your computer has been running

Instead of raw numbers, it displays everything in a clean, formatted box that refreshes every 10 seconds.

## How It Looks

When you run the app in a terminal, you’ll see:

```
╔═══════════════════════════════════════╗
║       CLOUD RESOURCE MONITOR        ║
╚═══════════════════════════════════════╝
CPU Usage       :  23%
Memory Usage    :  7.38%  (574 MB / 7.60 GB)
Disk Usage      :  0.16%  (1.65 GB / 1006 GB)
Uptime          :  1 hours, 41 minutes
Last Updated    :  14 Jun 2026, 14:09:57

Refreshes every 10 seconds. Press Ctrl+C to stop.
```

## Requirements

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- That's it. Nothing else needed.

## How To Run

**Step 1:** Install Docker Desktop from https://www.docker.com/products/docker-desktop

**Step 2:** Clone this repo
```
git clone https://github.com/MarkEbinaizer/cloud-resource-health-monitor-
cd cloud-resource-health-monitor-
```

**Step 3:** Run the app
```
docker run -it --rm markEbinaizer/cloud-health-monitor:latest
```
OR build locally:
```
docker-compose up --build
```

## Tech Stack

- Python (built-in libraries only)
- Docker
- Kubernetes
- GitHub Actions (CI/CD)

## About This Project

Built as part of my cloud computing and DevOps learning journey. This project demonstrates containerization with Docker, orchestration with Kubernetes, and CI/CD automation with GitHub Actions.