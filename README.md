# Cloud Resource Health Monitor

A lightweight Python application that monitors system resources (CPU, memory, disk usage, and uptime) and outputs the data as JSON. Designed for deployment in Docker and Kubernetes environments.

## Technologies Used

- **Python 3.10+** (using only built-in libraries)
- **Docker** for containerization
- **Kubernetes** for orchestration
- **GitHub Actions** for CI/CD (automated Docker image builds and pushes to DockerHub)

## Features

- Monitors CPU usage (percentage)
- Monitors memory usage (total, used, free, buffers, cached, and usage percentage)
- Monitors disk usage (total, used, free, and usage percentage)
- Reports system uptime in seconds
- Outputs structured JSON data to stdout
- Configurable monitoring interval via environment variable
- No external dependencies (only Python standard library)

## Architecture Diagram

```
+---------------------+
|   Host System       |
|  (Linux Server)     |
+----------+----------+
           |
           | Host ProcFS (/proc, /sys)
           v
+---------------------+
|  Health Monitor     |
|  Container/Pod      |
|  -----------------  |
|  | Python App     | |
|  | - CPU Monitor  | |
|  | - Memory Mon.  | |
|  | - Disk Monitor | |
|  | - Uptime Mon.  | |
|  -----------------  |
+---------------------+
           |
           | JSON Output to stdout
           v
+---------------------+
|   Logs / Monitoring |
|   (e.g., ELK,       |
|    Prometheus,      |
|    Grafana)         |
+---------------------+
```

## Local Development & Testing

### Prerequisites

- Docker installed
- Git (optional)

### Running with Docker Compose

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd cloud-resource-health-monitor
   ```

2. Start the service:
   ```bash
   docker-compose up --build
   ```

3. View the logs:
   ```bash
   docker-compose logs -f
   ```

   You should see JSON output similar to:
   ```json
   {
     "cpu_usage_percent": 15.2,
     "memory_usage": {
       "total": 8037024,
       "used": 3421184,
       "free": 4615840,
       "buffers": 212992,
       "cached": 1370112,
       "usage_percent": 42.6
     },
     "disk_usage": {
       "total": 1000000000,
       "used": 500000000,
       "free": 500000000,
       "usage_percent": 50.0
     },
     "uptime_seconds": 12345.67,
     "timestamp": 1623456789.123
   }
   ```

### Running with Docker directly

```bash
# Build the image
docker build -t health-monitor .

# Run the container
docker run --rm \
  --volume /proc:/host/proc:ro \
  --volume /sys:/host/sys:ro \
  --env MONITOR_INTERVAL=5 \
  health-monitor
```

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (e.g., minikube, EKS, GKE)
- `kubectl` configured to connect to your cluster
- Docker image pushed to a registry (see CI/CD section below)

### Steps

1. Build and push your Docker image to a registry (e.g., DockerHub):
   ```bash
   # Replace with your DockerHub username
   docker build -t <your-username>/health-monitor:latest .
   docker push <your-username>/health-monitor:latest
   ```

2. Update the image in `k8s/deployment.yaml`:
   ```yaml
   image: <your-username>/health-monitor:latest
   ```

3. Apply the Kubernetes manifests:
   ```bash
   kubectl apply -f k8s/configmap.yaml
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```

4. Verify the deployment:
   ```bash
   kubectl get pods
   kubectl logs -f <pod-name>
   ```

5. (Optional) Expose the service externally if needed (though the app outputs to logs, not a network port):
   ```bash
   kubectl expose deployment health-monitor-deployment --type=LoadBalancer --port=8080
   ```

## CI/CD Pipeline

This project includes a GitHub Actions workflow (`.github/workflows/docker-build.yml`) that automatically:

1. Triggers on every push to the `main` branch
2. Builds the Docker image
3. Pushes the image to DockerHub

### Setup

To enable the workflow, you need to add the following secrets to your GitHub repository:

- `DOCKERHUB_USERNAME`: Your DockerHub username
- `DOCKERHUB_TOKEN`: Your DockerHub personal access token (with write:packages scope)

## Configuration

The monitoring interval can be configured via the `MONITOR_INTERVAL` environment variable (in seconds). Default is 10 seconds.

In Docker:
```bash
docker run -e MONITOR_INTERVAL=5 health-monitor
```

In Kubernetes, the interval is set via the ConfigMap (`k8s/configmap.yaml`).

## Notes

- This application is designed for Linux systems as it relies on `/proc` and `/sys` filesystems.
- For Windows or macOS, additional platform-specific code would be required.
- The Docker container requires access to the host's `/proc` and `/sys` directories to read system metrics accurately.

## License

This project is open source and available under the MIT License.

*/