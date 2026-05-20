# Redpanda Three Node Cluster Compose Config Explained 🐼🐼🐼🚀

This Docker Compose file creates a **3-node Redpanda cluster** with **Redpanda Console UI**.

Unlike the single-node setup, here multiple brokers work together as a **cluster**.

This helps simulate a real production-like Kafka environment.

---

# Architecture Overview 🏗️

```text
                  +-------------------+
                  | Redpanda Console  |
                  | localhost:8080    |
                  +---------+---------+
                            |
                            v

     +------------- Redpanda Cluster 🌐 ------------+

     +-------------+ +-------------+ +-------------+
     | redpanda-0  | | redpanda-1  | | redpanda-2  |
     | Broker 0 🖥️ | | Broker 1 🖥️ | | Broker 2 🖥️ |
     +-------------+ +-------------+ +-------------+

```

Instead of one broker:

```text
Broker 0 + Broker 1 + Broker 2
```

All three work together.

---

## 🧩 1. Project Name

```yaml
name: redpanda-quickstart-three-broker
```

This is simply the project name.

---

# 🐼 Broker 1 (redpanda-0)

---

## Container Name

```yaml
container_name: redpanda-0
```

Creates first broker:

```text
Broker 0
```

---

## Kafka Port

```yaml
--kafka-addr internal://0.0.0.0:9092,external://0.0.0.0:19092
```

Internal:

```text
9092
```

External:

```text
19092
```

External port is different because multiple brokers cannot use same host port.

---

## Advertised Address

```yaml
--advertise-kafka-addr internal://redpanda-0:9092,external://localhost:19092
```

Tells applications:

Inside Docker:

```text
redpanda-0:9092
```

Outside Docker:

```text
localhost:19092
```

---

## RPC Address (Very Important) 📡

```yaml
--rpc-addr redpanda-0:33145
```

RPC = broker-to-broker communication.

Brokers use this address to talk with each other.

---

## Advertise RPC

```yaml
--advertise-rpc-addr redpanda-0:33145
```

Tells other brokers:

```text
Reach me here
```

---

## Seeds

```yaml
--seeds redpanda-0:33145
```

Seeds tell new brokers:

```text
Join cluster using this broker
```

Think of it like:

Broker-0 = team leader 👑

Other brokers first contact Broker-0.

---

# 🐼 Broker 2 (redpanda-1)

Almost same configuration.

Main difference:

```yaml
external://localhost:29092
```

Ports become:

```text
Kafka → 29092
Schema → 28081
Proxy → 28082
```

---

## Dependency

```yaml
depends_on:
  - redpanda-0
```

Broker-1 starts only after Broker-0.

Because Broker-1 joins Broker-0 cluster.

---

# 🐼 Broker 3 (redpanda-2)

Same idea.

Ports:

```text
Kafka → 39092
Schema → 38081
Proxy → 38082
```

---

## Dependency

```yaml
depends_on:
  - redpanda-1
```

Starts after Broker-1.

---

# Why Different Ports? 🤔

Multiple containers cannot expose same host ports.

Wrong ❌

```text
Broker1 → 9092
Broker2 → 9092
Broker3 → 9092
```

Correct ✅

```text
Broker1 → 19092
Broker2 → 29092
Broker3 → 39092
```

---

# Cluster Formation Flow 🔄

When cluster starts:

```text
redpanda-1
     ↓
Contacts seed broker

redpanda-0
     ↓
Joins cluster

redpanda-2
     ↓
Contacts seed broker
     ↓
Joins cluster
```

---

# Redpanda Console UI 🖥️

Console setup is almost identical to previous setup.

```yaml
kafka:
  brokers: ["redpanda-0:9092"]
```

Console connects to Broker-0.

Broker-0 already knows about the full cluster.

So console can discover:

- Broker-1
- Broker-2

automatically.

---

# Console Dependency

```yaml
depends_on:
   - redpanda-2
```

Console starts after all brokers become available.

---

# Why Use Three Brokers? 🚀

Single broker:

```text
1 machine
```

Three brokers:

```text
3 machines working together
```

Benefits:

✅ High availability  
✅ Fault tolerance  
✅ Better scalability  
✅ Load sharing  
✅ Production-like setup  

---

# Simple Summary 📝

This setup creates:

✔ Broker 0  
✔ Broker 1  
✔ Broker 2  
✔ Broker communication using RPC  
✔ Cluster formation using seed broker  
✔ Console UI at localhost:8080  

👉 In short: This Docker file creates a **real multi-broker Kafka-style Redpanda cluster with a visual UI 🚀**