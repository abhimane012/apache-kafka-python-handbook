# What is `CREATE TABLE` in ksqlDB? 📋⚡

In ksqlDB, `CREATE TABLE` is used to create a **table view on top of a Kafka topic**.

A table represents the **latest state of data**, not every event.

Unlike streams:

```text
Stream → continuous events 🌊
Table → current state 📋
```

---

## 🧠 Simple Meaning

A table keeps only the **latest value for each key**.

Example messages:

```text
user-1 → Online
user-1 → Away
user-1 → Offline
```

Stream sees:

```text
Online
Away
Offline
```

Table stores:

```text
user-1 → Offline
```

Only latest state remains.

---

## 🌍 Real-Life Analogy

Think of a classroom attendance board 📝

Students update status:

```text
John → Present
John → Lunch Break
John → Present
John → Absent
```

You usually care about:

```text
John → Absent
```

Current status only.

That is how a table works.

---

## Create Table Example ⚡

```sql
CREATE TABLE user_status (
   user_id VARCHAR PRIMARY KEY,
   status VARCHAR
)
WITH (
   KAFKA_TOPIC='user-status',
   VALUE_FORMAT='JSON'
);
```

---

## What Each Part Means 🧩

### Create table

```sql
CREATE TABLE
```

Create a state table.

---

### Columns

```sql
user_id VARCHAR
status VARCHAR
```

Defines fields.

---

### Primary key

```sql
PRIMARY KEY
```

Very important.

Table updates happen using keys.

---

### Kafka topic

```sql
KAFKA_TOPIC='user-status'
```

Read data from Kafka topic.

---

### Message format

```sql
VALUE_FORMAT='JSON'
```

Messages are JSON.

---

## Incoming Kafka Messages 📥

Topic:

```text
user-status
```

Messages:

```text
user-1 → Online
user-2 → Away
user-1 → Offline
```

---

## Table State 📋

After processing:

```text
user-1 → Offline
user-2 → Away
```

Only latest values remain.

---

## Query Table 👀

Run:

```sql
SELECT * FROM user_status EMIT CHANGES;
```

Output:

```text
user-1 | Offline
user-2 | Away
```

---

## Stream vs Table 🤔

| Stream 🌊 | Table 📋 |
|---|---|
| Stores every event | Stores latest state |
| Append-only | Updates existing state |
| Event history | Current view |

---

Example:

Stream:

```text
Order Created
Order Paid
Order Delivered
```

Table:

```text
Order Status → Delivered
```

---

## Why Tables Are Useful 🚀

### 1. Current State Tracking 📊

Useful for:

- User status 👤
- Inventory 📦
- Account balance 💰
- Device state 📡

---

### 2. Fast Lookups ⚡

Latest values available immediately.

---

### 3. Supports Joins 🔗

Tables can join with streams.

---

## Architecture Flow 🏗️

```text
Producer 🐍
      ↓
Kafka Topic 🗂️
      ↓
ksqlDB Table 📋
      ↓
Latest State
```

---

## 📝 Simple Summary

`CREATE TABLE`:

✔ Creates state view on Kafka topic  
✔ Stores latest value per key  
✔ Requires primary key  
✔ Useful for current state tracking  

---

## 🚀 Final Takeaway

👉 In short:

`CREATE TABLE` in ksqlDB = **Create a live table that continuously keeps the latest state of Kafka data 📋⚡**