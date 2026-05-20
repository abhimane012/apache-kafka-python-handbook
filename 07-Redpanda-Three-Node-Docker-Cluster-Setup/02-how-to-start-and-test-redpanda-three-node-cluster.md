# How to Start and Test Redpanda Three Node Cluster 🐼🐼🐼🚀

This guide shows how to start and test a **3-node Redpanda cluster** step by step.

You will:

- Start three Redpanda brokers 🖥️🖥️🖥️  
- Create a topic 🗂️  
- Produce messages 📤  
- Consume messages 📥  
- View everything visually in Console UI 🖥️  

---

## 🧱 Step 1: Start Three Node Cluster

```bash
docker compose -f docker-compose-redpanda-three-node-cluster.yaml up
```

### What this does:

- Starts Broker 0 🖥️  
- Starts Broker 1 🖥️  
- Starts Broker 2 🖥️  
- Builds a Redpanda cluster 🌐  
- Starts Console UI 🖥️  

👉 Now a complete multi-node Kafka-like system is running.

---

## 🐚 Step 2: Enter Broker Container

```bash
docker exec -it redpanda-0 bash
```

### What this does:

Opens terminal inside Broker-0.

👉 You can now run Redpanda (`rpk`) commands.

---

## 📊 Step 3: Verify Cluster

```bash
rpk cluster info
```

### What this does:

Shows cluster information.

You should see:

```text
Broker 0
Broker 1
Broker 2
```

This confirms all three brokers joined successfully 🎉

---

## 🗂️ Step 4: Create Topic With Replication

```bash
rpk topic create chat-room -r 3
```

### What this does:

Creates topic:

```text
chat-room
```

with:

```text
Replication factor = 3
```

Meaning:

```text
Broker-0 → copy
Broker-1 → copy
Broker-2 → copy
```

Each broker stores a copy of data.

👉 This improves fault tolerance 🔒

---

## 🔍 Step 5: Describe Topic

```bash
rpk topic describe chat-room
```

### What this does:

Displays topic details:

- partitions 📦  
- replicas 🔁  
- leader broker 👑  

Example:

```text
Partition 0
Leader: Broker-1
Replicas:
Broker-0
Broker-1
Broker-2
```

👉 You can see how Kafka distributes data.

---

## 📤 Step 6: Produce Messages

```bash
rpk topic produce chat-room
```

Type:

```text
hello cluster
my first message
```

### What this does:

Sends messages into topic.

Each line becomes a Kafka message 📩

---

## 📥 Step 7: Consume Message

```bash
rpk topic consume chat-room --num 1
```

### What this does:

Reads:

```text
1 message only
```

The option:

```bash
--num 1
```

means:

```text
Stop after reading one message
```

---

## 🚪 Step 8: Exit Container

```bash
exit
```

Returns to local machine terminal.

---

## 🌐 Step 9: Open Console UI

Open browser:

```text
http://localhost:8080
```

---

## 🖥️ Step 10: Observe Everything Visually

Inside Console UI you can now see:

### Cluster Information 🌐

```text
Broker-0
Broker-1
Broker-2
```

---

### Topic Created 🗂️

```text
chat-room
```

---

### Topic Details 📦

You can inspect:

- partitions  
- replicas  
- leader broker  

---

### Produced Messages 📩

Messages entered earlier:

```text
hello cluster
my first message
```

appear inside topic view.

---

## CLI → Cluster → UI Flow 🔄

```text
rpk command
      ↓
Redpanda Cluster
      ↓
Console UI
```

Whatever commands you run:

✔ topic created  
✔ replicas created  
✔ messages produced  
✔ cluster activity  

becomes visible in browser automatically.

---

## Final Summary 📝

With this setup you:

✔ Started 3 brokers  
✔ Created replicated topic  
✔ Produced messages  
✔ Consumed messages  
✔ Viewed everything using Console UI  

👉 In short: You just tested a **real multi-broker Kafka-style cluster with visual monitoring 🚀**