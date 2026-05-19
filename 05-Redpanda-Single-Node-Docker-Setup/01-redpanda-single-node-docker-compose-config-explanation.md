# Redpanda Single Node Docker Compose Explained 🐼🚀

This Docker Compose file starts a **single Redpanda broker** (Kafka-compatible system) on your machine.

Let’s break it down step by step in a very simple way.

---

## 🧱 1. Basic Setup

```yaml
name: redpanda-quickstart-one-broker
```

👉 This is just the **project name** for your setup.  
It helps identify this Redpanda environment.

---

## 🧩 2. Services Section

```yaml
services:
  redpanda:
```

👉 This means we are running **one service called Redpanda** inside Docker.

---

## 🐳 3. Docker Image

```yaml
image: docker.redpanda.com/redpandadata/redpanda:v26.1.8
```

👉 This tells Docker:

- Download Redpanda software
- Use version `v26.1.8`

Think of it like downloading a ready-made app 📦

---

## 📦 4. Container Name

```yaml
container_name: redpanda-0
```

👉 This gives a name to the running container.

Instead of a random Docker name, we call it:

- `redpanda-0`

---

## ▶️ 5. Start Command

```yaml
command:
  - redpanda start
```

👉 This starts the Redpanda server inside the container.

---

## ⚙️ 6. Performance Settings

```yaml
  - --smp 1
```

👉 Uses **1 CPU core**

- Keeps it lightweight
- Good for local development

---

```yaml
  - --overprovisioned
```

👉 Tells Redpanda:

- “This is a small dev machine”
- Allows relaxed resource usage

---

## 🌐 7. Kafka API Ports (Important!)

```yaml
  - --kafka-addr internal://0.0.0.0:19092,external://0.0.0.0:9092
```

👉 This sets Kafka communication ports:

### Internal:
- `19092` → used inside Docker network

### External:
- `9092` → used by your local Python apps

📌 Example:
```text
Python app → localhost:9092 → Redpanda
```

---

## 📣 8. Kafka Address Exposure

```yaml
  - --advertise-kafka-addr internal://redpanda:19092,external://localhost:9092
```

👉 This tells clients:

- Inside Docker → use `redpanda:19092`
- Outside Docker → use `localhost:9092`

📌 Why needed?
So applications know **how to connect correctly**.

---

## 🌐 9. Pandaproxy (HTTP API)

```yaml
  - --pandaproxy-addr internal://0.0.0.0:18082,external://0.0.0.0:8082
```

👉 Enables **HTTP-based Kafka access**

- Internal: `18082`
- External: `8082`

📌 Use case:
- Call Kafka using REST APIs (instead of Kafka protocol)

---

```yaml
  - --advertise-pandaproxy-addr internal://redpanda:18082,external://localhost:8082
```

👉 Same idea:

- Docker network → `redpanda:18082`
- Local machine → `localhost:8082`

---

## 🧾 10. Schema Registry

```yaml
  - --schema-registry-addr internal://0.0.0.0:18081,external://0.0.0.0:8081
```

👉 This enables **schema management for messages**

Used for:
- Structuring data (like JSON format rules)
- Ensuring producers/consumers agree on data format

Ports:
- Internal: `18081`
- External: `8081`

---

## 🚪 11. Port Mapping

```yaml
ports:
  - 8081:8081
  - 8082:8082
  - 9092:9092
```

👉 This exposes Redpanda services to your local machine:

| Local Port | Purpose |
|------------|--------|
| 9092 | Kafka API (Python clients use this) |
| 8082 | HTTP Proxy (Pandaproxy) |
| 8081 | Schema Registry |

---

## 🧠 Simple Flow

```text
Python App 🐍
     ↓ (localhost:9092)
Redpanda Broker 🐼
     ↓
Topics + Partitions 📦
```

---

## 📝 Final Summary

This Docker setup:

✔ Starts a single Redpanda broker  
✔ Exposes Kafka-compatible port (9092)  
✔ Enables HTTP API (8082)  
✔ Enables Schema Registry (8081)  
✔ Configures internal + external communication  

👉 In short:  
This file runs a **local Kafka-like system (Redpanda) so you can develop and test easily on your machine** 🚀