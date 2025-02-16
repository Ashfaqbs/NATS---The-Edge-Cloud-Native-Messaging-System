# NATS JetStream Commands:

## 1. Managing Streams

### **a. Create a Stream**

Creates a stream with specified subjects and configuration.  
*Example: Create a stream named `order_stream` that stores messages on the subject `"orders"`.*

```bash
nats stream add order_stream --subjects "orders"
```

*During interactive prompts we might see:*

- **Storage:** file (persistent on disk)
- **Replication:** 1 (for single-server setups; increase in clusters)
- **Retention Policy:** Limits (retains messages until limits are reached)
- **Discard Policy:** Old (removes the oldest messages when limits are exceeded)
- **Stream Messages Limit:** -1 (unlimited)
- **Per Subject Messages Limit:** -1 (unlimited)
- **Total Stream Size:** -1 (unlimited)
- **Message TTL:** -1 (no expiration)
- **Max Message Size:** -1 (unlimited)
- **Duplicate Tracking Window:** (e.g., 2m0s)
- **Allow Purge:** Yes

### **b. Create a DLQ Stream**

Creates a dedicated stream for dead-letter messages.  
*Example: Create a stream named `order_dlq` that uses subject `"orders.dlq"`.*

```bash
nats stream add order_dlq --subjects "orders.dlq"
```

*Configuration is similar to the main stream, ensuring failed messages are captured.*

### **c. List Streams**

Lists all the streams available in the JetStream account.

```bash
nats stream ls
```

### **d. Get Stream Information**

Displays detailed configuration and state information about a specific stream.

```bash
nats stream info order_stream
```

### **e. Purge a Stream**

Removes all messages from a stream without deleting the stream itself.  
*Example: Purge all messages from `order_stream`.*

```bash
nats stream purge order_stream
```

### **f. Delete a Stream**

Removes a stream and all of its stored messages.

```bash
nats stream rm order_stream
```

---

## 2. Managing Consumers

### **a. Create a Consumer**

Creates a consumer for a stream. For pull-based consumers, use the `--pull` flag.  
*Example: Create a durable consumer named `order_consumer` for `order_stream` with an acknowledgment wait of 2 seconds and a maximum of 3 deliveries.*

```bash
nats consumer add order_stream order_consumer --wait 2s --max-deliver 3 --pull
```

*Interactive prompts may ask for:*

- **Start Policy:** (e.g., `all`)
- **Acknowledgment Policy:** (e.g., `all` or `explicit`)
- **Replay Policy:** (e.g., `instant`)
- **Filter by Subjects:** (leave blank for all)
- **Maximum Acknowledgments Pending:** (e.g., 1000)
- **Add a Retry Backoff Policy:** (Yes/No)

### **b. List Consumers**

Lists all consumers for a given stream.  
*Example: List consumers for `order_stream`.*

```bash
nats consumer ls order_stream
```

### **c. Get Consumer Information**

Shows details for a specific consumer.

```bash
nats consumer info order_stream order_consumer
```

### **d. Remove a Consumer**

Deletes a consumer from a stream.  
*Example: Remove the consumer named `order_consumer` from `order_stream`.*

```bash
nats consumer rm order_stream order_consumer
```

### **e. Fetch Next Message**

For pull-based consumers, we can fetch the next available message.  
*Example: Fetch the next message from `order_consumer` in `order_stream`.*

```bash
nats consumer next order_stream order_consumer
```

---

## 3. Working with Messages

### **a. Publish a Message**

Publishes a message to a subject, which is then captured by the stream if the subject matches.  
*Example: Publish a message to the `"orders"` subject.*

```bash
nats pub orders "pass Order 101"
```

### **b. Subscribe to a Subject**

Subscribes to a subject to see messages in real time. This is useful for debugging or monitoring.  
*Example: Subscribe to the DLQ subject to view failed messages.*

```bash
nats sub orders.dlq
```

---

## 4. Additional Useful Commands

### **a. Update a Stream or Consumer**

While certain configurations are immutable once set, we can often update a stream’s configuration by re-creating it (after deletion) or by using an update command if available.  
*For consumers, sometimes we must remove and re-add them with the new configuration.*

### **b. Check Server or Context Information**

Although not strictly part of JetStream management, these commands help verify our current configuration or context:

- **List Contexts:**

  ```bash
  nats context ls
  ```

- **Set a Context:**

  ```bash
  nats context select <context_name>
  ```

---

## Example Workflow Recap

1. **Create Main Stream and DLQ:**

   ```bash
   nats stream add order_stream --subjects "orders"
   nats stream add order_dlq --subjects "orders.dlq"
   ```

2. **Create a Consumer:**

   ```bash
   nats consumer add order_stream order_consumer --wait 2s --max-deliver 3 --pull
   ```

3. **Publish Messages:**

   ```bash
   nats pub orders "pass Order 1"
   nats pub orders "fail Order 2"
   ```

4. **Subscribe to DLQ to Monitor Failed Messages:**

   ```bash
   nats sub orders.dlq
   ```

5. **View Stream or Consumer Information:**

   ```bash
   nats stream info order_stream
   nats consumer info order_stream order_consumer
   ```

6. **Purge or Delete Streams/Consumers as Needed:**

   ```bash
   nats stream purge order_stream
   nats consumer rm order_stream order_consumer
   nats stream rm order_stream
   ```

---

These commands give we a robust set of tools for managing our NATS JetStream environment from the CLI. They allow we to create, modify, monitor, and clean up streams and consumers efficiently. If we have any further questions or need more examples, feel free to ask!

---
