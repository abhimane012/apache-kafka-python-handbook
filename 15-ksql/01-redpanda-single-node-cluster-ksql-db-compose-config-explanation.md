# Redpanda Single Node + ksqlDB Compose Config Explained 🐼⚡🧠

This Docker Compose file creates:

✔ Single Redpanda broker 🐼  
✔ Redpanda Console UI 🖥️  
✔ ksqlDB Server ⚡  
✔ ksqlDB CLI 💻  

The Redpanda + Console setup is mostly same as previous examples.

Here we will focus mainly on the **ksqlDB part**.

---

# First: What is ksqlDB? 🤔

**ksqlDB** is a SQL engine for Kafka.

It lets you use **SQL queries on real-time Kafka data**.

Instead of writing Java or Python code:

```python
read message
filter message
transform message
aggregate message
```

You can write:

```sql
SELECT * FROM chat_room;
```

---

## 🌍 Real-Life Analogy

Think of Kafka as a flowing river 🌊

Normally:

You write code to analyze water flow.

With ksqlDB:

You simply ask questions:

```sql
Show all messages
Count users
Filter events
```

Using SQL.

---

# Architecture Overview 🏗️

```text
Producer 🐍
      ↓
Redpanda 🐼
      ↓
ksqlDB Server ⚡
      ↓
SQL Queries
      ↓
Redpanda Console 🖥️
```

---

# 🧩 ksqlDB Server Service

```yaml
ksqldb-server:
```

Creates:

```text
Real-time SQL server for Kafka
```

---

## 🐳 Docker Image

```yaml
image: confluentinc/ksqldb-server
```

Downloads ksqlDB server software.

Think:

```text
Kafka + SQL engine
```

---

## Dependency

```yaml
depends_on:
   - redpanda
```

ksqlDB starts only after Redpanda starts.

Because:

```text
ksqlDB needs Kafka running
```

---

## Port Mapping

```yaml
ports:
   - 8088:8088
```

Exposes:

```text
localhost:8088
```

This becomes ksqlDB API endpoint.

Applications can connect here.

---

# Environment Variables ⚙️

---

## Kafka Connection

```yaml
KSQL_BOOTSTRAP_SERVERS: redpanda:19092
```

Tells ksqlDB:

```text
Connect to Kafka broker here
```

Broker address:

```text
redpanda:19092
```

---

## Listener Address

```yaml
KSQL_LISTENERS: "http://0.0.0.0:8088"
```

Tells ksqlDB:

```text
Open port 8088
Wait for requests
```

This is similar to:

```text
kafka-addr
```

for Kafka.

---

## Schema Registry Connection

```yaml
KSQL_KSQL_SCHEMA_REGISTRY_URL: http://redpanda:18081
```

Tells ksqlDB:

```text
Schema Registry lives here
```

Needed because ksqlDB often works with:

- Avro
- JSON Schema
- Protobuf

---

## Buffering Configuration

```yaml
KSQL_CACHE_MAX_BYTES_BUFFERING: 0
```

Disables internal buffering.

Meaning:

```text
Process results immediately
```

Useful for learning and development.

Without this:

Results may appear delayed.

---

# 🧩 ksqlDB CLI Service

```yaml
ksqldb-cli:
```

Creates command-line interface.

Think:

```text
SQL terminal for Kafka
```

---

## Docker Image

```yaml
image: confluentinc/cp-ksqldb-server
```

Provides tools needed to run CLI.

---

## Dependency

```yaml
depends_on:
   - ksqldb-server
```

CLI starts after server.

Because:

```text
CLI talks to ksqlDB server
```

---

## Entrypoint

```yaml
entrypoint: /bin/sh
```

Starts shell terminal.

Allows you to manually run:

```bash
ksql http://ksqldb-server:8088
```

---

## Interactive Terminal

```yaml
tty: true
```

Keeps container interactive.

Without this:

Container exits immediately ❌

---

# How Everything Connects 🔄

```text
Python Producer 🐍
      ↓
Redpanda Topic 🐼
      ↓
ksqlDB reads stream ⚡
      ↓
SQL query runs
      ↓
Result shown
```

---

# Example Query 🧠

Suppose topic:

```text
chat-room
```

You can write:

```sql
SELECT * FROM chat_room EMIT CHANGES;
```

Meaning:

```text
Show live messages continuously
```

---

# Why Use ksqlDB? 🚀

✅ SQL instead of application code  
✅ Real-time filtering  
✅ Real-time aggregation  
✅ Stream processing  
✅ Easy for beginners  

---

# Final Summary 📝

This setup adds:

✔ Redpanda broker 🐼  
✔ Console UI 🖥️  
✔ ksqlDB server ⚡  
✔ SQL command-line tool 💻  

👉 In short:

This setup lets you **query and process Kafka streams using SQL instead of writing code 🚀**