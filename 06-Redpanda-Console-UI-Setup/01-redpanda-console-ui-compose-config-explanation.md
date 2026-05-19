# Redpanda Console UI (Compose Config Explanation) 🖥️🐼

This explains only the **Redpanda Console part**, which gives you a **web UI to view Kafka/Redpanda data visually**.

Everything else in the file (Redpanda broker setup) is same as the single-node setup.

---

## 🧩 1. Console Service

```yaml
redpanda-console:
```

👉 This defines a **new service called Redpanda Console**

- It runs a **web-based UI**
- Helps you visually manage topics, messages, and cluster

---

## 🐳 2. Console Docker Image

```yaml
image: docker.redpanda.com/redpandadata/console:v3.7.2
```

👉 This downloads and runs the **Redpanda Console application**

Think of it like:

🧠 Kafka CLI (rpk) → command line  
🖥️ Redpanda Console → browser UI (easy visual tool)

---

## ⚙️ 3. Entry Point Setup

```yaml
entrypoint: /bin/sh
```

👉 This means:

- Start a shell inside the container first  
- Then run custom commands

---

## ▶️ 4. Command Execution

```yaml
command: -c 'echo "$$CONSOLE_CONFIG_FILE" > /tmp/config.yml; /app/console'
```

### What this does step by step:

1. Takes environment config (`CONSOLE_CONFIG_FILE`)  
2. Writes it into a file → `/tmp/config.yml`  
3. Starts the console app → `/app/console`  

👉 Basically: “create config file → start UI”

---

## 🌍 5. Environment Variables

### 📌 CONFIG_FILEPATH

```yaml
CONFIG_FILEPATH: /tmp/config.yml
```

👉 Tells console:

- “Use this config file to connect to Kafka and services”

---

### 📌 CONSOLE_CONFIG_FILE (Most Important Part)

This defines **how the UI connects to Redpanda services**.

---

## 🔗 Kafka Connection

```yaml
kafka:
  brokers: ["redpanda-0:19092"]
```

👉 This tells console:

- Connect to Redpanda broker inside Docker network  
- `redpanda-0:19092` = internal Kafka address

📌 Meaning:
- Console reads topics/messages from this broker

---

## 📊 Schema Registry Connection

```yaml
schemaRegistry:
  enabled: true
  urls: ["http://redpanda-0:18081"]
```

👉 This enables schema support in UI:

- View structured message formats (JSON schema, Avro, etc.)
- Helps understand message structure easily

---

## 🛠️ Redpanda Admin API

```yaml
redpanda:
  adminApi:
    enabled: true
    urls: ["http://redpanda-0:9644"]
```

👉 This allows console to:

- View cluster health 🩺  
- Check broker status 🖥️  
- Access internal admin metrics 📊  

---

## 🚪 6. UI Port Exposure

```yaml
ports:
  - 8080:8080
```

👉 This exposes the **web UI to your browser**

### You can open:

```text
http://localhost:8080
```

👉 This is where you:

- View topics 🗂️  
- Read messages 📥  
- Produce messages 📤  
- Monitor cluster 🌐  

---

## 🔗 7. Dependency

```yaml
depends_on:
  - redpanda
```

👉 This means:

- Start Redpanda first 🐼  
- Then start Console 🖥️  

Because UI needs Kafka running to connect.

---

## 🧠 Simple Flow

```text
Redpanda Broker 🐼 → stores data
        ↓
Redpanda Console 🖥️ → visualizes data
        ↓
Browser (localhost:8080) 🌐 → user interacts
```

---

## 📝 Final Summary

Redpanda Console:

✔ Web UI for Kafka/Redpanda  
✔ Connects to broker (19092)  
✔ Reads schema registry (18081)  
✔ Uses admin API (9644)  
✔ Runs on browser at localhost:8080  

👉 In short: Redpanda Console = **A browser-based UI to view and manage Kafka data easily 🖥️🚀**