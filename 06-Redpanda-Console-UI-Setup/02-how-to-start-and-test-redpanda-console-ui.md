# How to Start and Test Redpanda Console UI 🐼🖥️🚀

This guide shows how to **start Redpanda + Console UI** and test everything step by step.

You will:
- Start Redpanda using Docker 🐳  
- Use CLI to create and send messages 📤  
- View everything in a browser UI 🌐  

---

## 🧱 Step 1: Start Redpanda + Console

```bash
docker compose -f docker-compose-redpanda-console-ui.yaml up
```

### What this does:

- Starts Redpanda broker 🐼  
- Starts Redpanda Console UI 🖥️  
- Exposes Kafka + UI ports  
- Prepares full environment for testing  

👉 After this step, everything is running.

---

## 🐚 Step 2: Enter Redpanda Container

```bash
docker exec -it redpanda-0 bash
```

### What this does:

- Opens terminal inside Redpanda container  
- Lets you run Kafka commands using `rpk`  

👉 Think of it like entering the Kafka server room 🏢

---

## 📊 Step 3: Check Cluster Info

```bash
rpk cluster info
```

### What this does:

- Confirms Redpanda cluster is running  
- Shows broker and cluster details  

👉 First check to ensure system is working properly.

---

## 🗂️ Step 4: Create Topic

```bash
rpk topic create chat-room
```

### What this does:

- Creates a topic called `chat-room`  
- This is where messages will be stored  

👉 Like creating a chat group 💬

---

## 🔍 Step 5: Describe Topic

```bash
rpk topic describe chat-room
```

### What this does:

- Shows topic details  
- Includes partitions and configuration  

👉 Helps you understand how Kafka stores data 📦

---

## 📤 Step 6: Produce Messages

```bash
rpk topic produce chat-room
```

### What this does:

- Lets you send messages into the topic  
- Type messages manually in terminal  

Example:

```text
hello world
my first kafka message
```

👉 Each line becomes a Kafka message 📩

---

## 📥 Step 7: Consume Messages

```bash
rpk topic consume chat-room
```

### What this does:

- Reads messages from the topic  
- Shows real-time incoming messages  

👉 You can see everything that was produced 📡

---

## 🚪 Step 8: Exit Container

```bash
exit
```

### What this does:

- Leaves the Redpanda container terminal  
- Returns to your local system  

---

## 🌐 Step 9: Open Redpanda Console UI

Open your browser:

```text
http://localhost:8080
```

---

## 🖥️ Step 10: View Everything in UI

In the Redpanda Console UI, you can:

- View cluster status 🌐  
- See topics 🗂️  
- View messages 📥  
- Produce messages from UI 📤  
- Monitor partitions and brokers 📊  

---

## 🔄 How CLI and UI Work Together

Everything you did in CLI is visible in UI:

```text
CLI (rpk commands) → Redpanda Cluster → Console UI (browser)
```

So:

- Topic created in CLI → appears in UI 🗂️  
- Messages produced → visible in UI 📩  
- Messages consumed → tracked in UI 📊  

---

## 🧠 Final Flow Summary

```text
Start system 🐼
   ↓
Create topic 🗂️
   ↓
Produce messages 📤
   ↓
Consume messages 📥
   ↓
View everything in browser 🖥️
```

---

## 📝 Final Summary

With this setup, you:

✔ Start Redpanda + Console UI  
✔ Create and manage topics using CLI  
✔ Produce and consume messages  
✔ Visualize everything in browser  

👉 In short: You build a **complete Kafka-like system with both CLI + UI visibility 🚀**