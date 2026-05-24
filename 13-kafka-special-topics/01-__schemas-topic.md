# What is the `_schemas` Topic in Kafka? 🗂️📘

The `_schemas` topic is a **special internal Kafka topic used by Schema Registry** to store all schema information.

It is NOT a normal user topic.

It is used internally to manage schemas safely and reliably.

---

## 🧠 Simple Meaning

Whenever you define a schema in Kafka (using Schema Registry), Kafka needs to store it somewhere.

That storage place is:

```text
_schemas topic
```

👉 It acts like a **database for schemas inside Kafka itself**.

---

## 🌍 Real-Life Analogy

Think of a library 📚

- Books = schemas 📘  
- Library catalog system = `_schemas` topic 🗂️  

When you search or store a book, the catalog keeps track of everything.

Similarly:

```text
_schemas = catalog of all Kafka schemas
```

---

## 🔄 Why Does Kafka Need `_schemas` Topic?

Because Schema Registry needs to:

- Store schema versions 📘  
- Track schema changes 🔄  
- Enforce compatibility rules 🛡️  
- Retrieve schema quickly ⚡  

Instead of using an external database, it uses Kafka itself.

---

## 🧩 What Is Stored Inside `_schemas`?

It stores:

- Schema definitions 📄  
- Schema versions 🔢  
- Metadata (subject, id, compatibility rules) 🧠  
- Evolution history 🔄  

Example stored internally:

```json
{
  "subject": "user-topic-value",
  "version": 3,
  "schema": "{...json schema...}"
}
```

---

## 📦 How It Works (Step-by-Step)

### Step 1: Producer sends schema

```text
User event schema
```

---

### Step 2: Schema Registry checks compatibility

```text
Allowed? ❓
```

---

### Step 3: Schema stored in Kafka

```text
_schemas topic
```

---

### Step 4: Schema ID returned

```text
Schema ID = 15
```

---

### Step 5: Messages use schema ID instead of full schema

```text
Message → {schemaId: 15, data: ...}
```

---

## ⚙️ Why Use Kafka Topic Instead of Database?

### 1. Durability 💾

Kafka ensures data is stored safely.

---

### 2. Replication 🔁

Schemas are replicated across brokers.

---

### 3. High Availability 🌐

Even if one broker fails, schemas remain.

---

### 4. Ordering 📊

Kafka guarantees order of schema changes.

---

## 🔐 Is `_schemas` Visible to Users?

Normally:

❌ Hidden from users  
❌ Not meant for direct use  

But you can technically view it using:

```bash
rpk topic list
```

You may see:

```text
_schemas
```

---

## ⚠️ Important Warning

You should NEVER:

- Delete `_schemas` topic ❌  
- Modify it manually ❌  
- Produce messages directly ❌  

Doing so can break Schema Registry.

---

## 🧠 Simple Flow

```text
Producer
   ↓
Schema Registry
   ↓
_schemas topic 🗂️
   ↓
Schema stored safely
   ↓
Consumer uses schema ID
```

---

## 📝 Simple Summary

The `_schemas` topic:

✔ Stores all schema definitions  
✔ Maintains schema versions  
✔ Used internally by Schema Registry  
✔ Ensures durability and replication  
✔ Acts like Kafka’s schema database  

---

## 🚀 Final Takeaway

👉 In short:

`_schemas` = **Internal Kafka topic used by Schema Registry to store and manage all schemas safely 📘🗂️**