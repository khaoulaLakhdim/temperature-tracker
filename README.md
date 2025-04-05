# 📡 IoT Temperature Logger – Progressive Project

This project simulates an IoT system for registering devices and logging temperature readings, developed in **progressive stages**. Each stage introduces new technologies and best practices — from CLI to cloud-ready deployments.

---

## 🧱 Project Stages

### ✅ Stage 1 – CLI App (Python + PostgreSQL)

- Command-line app built with Python
- Register devices
- Log temperature readings
- Generate statistical reports: min, max, average, last reading
- Data stored in a local PostgreSQL database
- Database schema includes automatic trigger updates for device stats

---

### 🚧 Stage 2 – RESTful API + Docker (In Progress)

- Web API using FastAPI (or Flask)
- Dockerized Python + PostgreSQL setup
- Expose endpoints to register, log, and retrieve device data
- Deployable anywhere (Docker Compose)

> 📂 Coming soon: `Stage-2-API-Docker/`

---

## 🧰 Tech Stack

- Python
- PostgreSQL
- psycopg2
- FastAPI (planned)
- Docker & Docker Compose (planned)
- Git & GitHub
...
