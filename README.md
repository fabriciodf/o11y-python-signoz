# 🐍 FastAPI + OpenTelemetry + SigNoz (Local Observability Stack)

This project demonstrates how to instrument a Python FastAPI application using **OpenTelemetry**, and export **logs, metrics, and traces** to a local instance of [**SigNoz**](https://signoz.io/), an open-source APM alternative.

---

## 📦 Stack Overview

- ⚙️ **FastAPI** app with automatic OpenTelemetry instrumentation  
- 📊 **SigNoz** (runs locally via Docker)  
- 🚢 Containerized with `docker-compose`  
- 🛠️ `run.sh` automates setup and cleanup  

---

## 🚀 How to Run Locally

### 1. Clone this repository

```bash
git clone git@github.com:fabriciodf/o11y-python-signoz.git
cd o11y-python-signoz
```


### 2. Run everything with the provided script
```bash
chmod +x run.sh
./run.sh
```

This will:

- Clone and start the SigNoz stack
- Clean up any existing containers/images
- Build and run your FastAPI app

### 3. Access the services
- 📱 FastAPI: http://localhost:8000
- 📈 SigNoz UI: http://localhost:3301



## 4. 📁 Project Structure
```arduino
.
├── Dockerfile
├── docker-compose.yml
├── main.py
├── run.sh
└── requirements.txt
```

## 5. 🔍 Observability Details

The FastAPI app is instrumented via environment variables:

```env
OTEL_EXPORTER_OTLP_ENDPOINT=http://host.docker.internal:4317
OTEL_TRACES_EXPORTER=otlp
OTEL_METRICS_EXPORTER=otlp
OTEL_LOGS_EXPORTER=otlp
```

host.docker.internal works on Docker Desktop (WSL/Windows/macOS).
On native Linux, replace it with the bridge IP (usually 172.17.0.1).


## 6. 🛠️ Built With

- FastAPI
- OpenTelemetry Python SDK
- SigNoz
- Docker Compose

## 7. 📜 License

MIT License © fabriciodf