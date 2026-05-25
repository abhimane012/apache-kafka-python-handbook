# How to Start and Test Redpanda Single Node Cluster with ksqlDB 🚀🐼⚡

In this section we will:

✔ Start Redpanda 🐼  
✔ Start Console UI 🖥️  
✔ Start ksqlDB Server ⚡  
✔ Open ksqlDB CLI 💻  
✔ Connect to ksqlDB  
✔ Create Kafka topic  
✔ Verify topic using SQL commands  

---

# Step 1: Start All Containers 🐳

Run:

```bash
docker compose -f docker-compose-redpanda-single-node-ksql-db.yaml up
```

This starts:

```text
Redpanda Broker
Redpanda Console
ksqlDB Server
ksqlDB CLI
```

Docker will download images if running for the first time.

Wait until containers become healthy.

---

# Step 2: Open ksqlDB CLI Container 💻

Open another terminal and enter:

```bash
docker exec -it ksqldb-cli /bin/sh
```

Explanation:

```text
docker exec
```

Runs commands inside a container.

```text
-it
```

Starts interactive terminal mode.

```text
ksqldb-cli
```

Container name.

```text
/bin/sh
```

Opens shell.

Now you are inside:

```text
ksqldb-cli container
```

---

# Step 3: Connect CLI to ksqlDB Server ⚡

Run:

```bash
ksql http://ksqldb-server:8088
```

Explanation:

```text
ksql
```

Starts SQL terminal.

---

```text
http://ksqldb-server:8088
```

Address of ksqlDB server.

If successful you will see:

```text
ksql>
```

This means:

```text
Connected successfully ✅
```

---

# Step 4: Create Topic on Redpanda 🐼

Open another terminal.

Go inside Redpanda container:

```bash
docker exec -it redpanda bash
```

Create topic:

```bash
rpk topic create chat-room
```

Expected:

```text
TOPIC
chat-room
```

Topic created successfully.

---

# Step 5: Return to ksqlDB Terminal ⚡

Back inside:

```text
ksql>
```

Run:

```sql
show topics;
```

---

Explanation:

```sql
show topics;
```

Asks:

```text
Show all Kafka topics available
```

---

Expected output:

```text
chat-room
```

You should see your newly created topic.

Success 🎉

---

# What Happened Internally? 🧠

```text
Redpanda Topic Created
          ↓
ksqlDB connects to Redpanda
          ↓
ksqlDB fetches topic metadata
          ↓
show topics displays results
```

---

# Optional Verification Using Console UI 🖥️

Open browser:

```text
http://localhost:8080
```

Inside Console UI you can also see:

✔ Topics  
✔ Partitions  
✔ Brokers  
✔ Messages  

---

# Architecture Flow 🏗️

```text
Docker Compose
      ↓
Redpanda 🐼
      ↓
ksqlDB Server ⚡
      ↓
ksqlDB CLI 💻
      ↓
SQL Commands
```

---

# Final Summary 📝

Commands used:

Start cluster:

```bash
docker compose -f docker-compose-redpanda-single-node-ksql-db.yaml up
```

Open CLI:

```bash
docker exec -it ksqldb-cli /bin/sh
```

Connect:

```bash
ksql http://ksqldb-server:8088
```

Create topic:

```bash
rpk topic create chat-room
```

Verify:

```sql
show topics;
```

---

🚀 You now have a working Redpanda + ksqlDB setup where you can explore Kafka topics using SQL.