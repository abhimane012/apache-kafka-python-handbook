# How to Start and Test Redpanda Single Node 🐼🚀

This guide shows how to **run Redpanda locally using Docker** and test it step by step in a very simple way.

---

## 🧱 Step 1: Start Redpanda Container

```bash
docker compose -f docker-compose-redpanda-single-node.yaml up
```

### What this does:

- Starts Redpanda using Docker Compose 🐳  
- Creates a single broker (server) 🖥️  
- Exposes Kafka-compatible ports (9092, 8081, 8082) 🌐  

👉 After this step, Redpanda is running on your machine.

---

## 🐚 Step 2: Enter the Redpanda Container

```bash
docker exec -it redpanda-0 bash
```

### What this does:

- Opens a terminal inside the running Redpanda container  
- Allows you to run Redpanda commands (`rpk`) directly  

👉 Think of it like “entering the Kafka server room” 🏢

---

## 📊 Step 3: Check Cluster Status

```bash
rpk cluster info
```

### What this does:

- Shows basic information about your Redpanda cluster  
- Confirms that the broker is running properly  

👉 If everything is correct, you’ll see cluster details like ID, nodes, etc.

---

## 🗂️ Step 4: Create a Topic

```bash
rpk topic create chat-room
```

### What this does:

- Creates a new topic called `chat-room`  
- This is where messages will be stored  

👉 Think of it like creating a chat group 💬

---

## 🔍 Step 5: Describe the Topic

```bash
rpk topic describe chat-room
```

### What this does:

- Shows details about the topic  
- Includes partitions, replication, and configuration  

👉 Helps you understand how the topic is structured 📦

---

## 📤 Step 6: Produce Messages

```bash
rpk topic produce chat-room
```

### What this does:

- Lets you send messages into the topic  
- You can type messages manually  

Example:

```text
hello kafka
this is my first message
```

👉 Each line becomes a message in Kafka/Redpanda 📩

---

## 📥 Step 7: Consume Messages

```bash
rpk topic consume chat-room
```

### What this does:

- Reads messages from the topic  
- Shows messages in real-time as they arrive  

👉 You will see all produced messages here 📡

---

## 🔄 Full Flow Summary

```text
Start Redpanda 🐼
        ↓
Enter container 🐚
        ↓
Create topic 🗂️
        ↓
Produce messages 📤
        ↓
Consume messages 📥
```

---

## 🧠 Final Summary

With these steps, you:

✔ Start a local Redpanda cluster  
✔ Create a Kafka-like topic  
✔ Send messages into it  
✔ Read messages in real-time  

👉 In short: You just built a **mini real-time messaging system on your local machine using Redpanda 🚀**