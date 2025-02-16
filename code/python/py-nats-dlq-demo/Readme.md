## 🌟 **NATS Stream and DLQ Setup**

- we have not yet implemented NAK and retry logic.

✅ **Main Stream:**  
We created a stream called `order_stream` to handle order messages.

```bash
nats stream add order_stream --subjects "orders"
```

- **Storage:** File (messages persist across server restarts).  
- **Replication:** 1 (no redundancy — stream exists on a single server).  
- **Retention Policy:** Limits (messages are retained until certain limits like message count or storage size are reached).  
- **Discard Policy:** Old (oldest messages are discarded when limits are reached).  
- **Maximum Messages/Size/TTL:** Unlimited.

✅ **DLQ Stream:**  
We created a second stream called `order_dlq` to act as a dead-letter queue (DLQ) for failed messages.

```bash
nats stream add order_dlq --subjects "orders.dlq"
```

- Same retention, discard, and storage settings as the main stream.
- This stream collects failed orders, allowing for reprocessing or investigation later.

✅ **Consumer:**  
We created a durable pull-based consumer called `order_consumer` to process messages from `order_stream`.

```bash
nats consumer add order_stream order_consumer --wait 2s --max-deliver 3 --pull
```

- **Ack Wait:** 2 seconds (if a message isn’t acknowledged in 2 seconds, it’s redelivered).  
- **Max Deliver:** 3 (after 3 failed deliveries, the message is marked for DLQ).  
- **Pull Mode:** Consumer explicitly requests messages from the stream.

---

## 🚀 **Producer Logs**

✅ **Producer Behavior:**  
- Publishes messages to the `order_stream` on the `orders` subject.
- Messages randomly contain either `"pass Order X"` or `"fail Order Y"`.
- Successful publication returns a `PubAck` with the stream name and sequence number.

Example logs:

```
Published: fail Order 1 (Ack: PubAck(stream='order_stream', seq=1))
Published: pass Order 3 (Ack: PubAck(stream='order_stream', seq=3))
Published: fail Order 4 (Ack: PubAck(stream='order_stream', seq=4))
```

---

## ⚙️ **Consumer Logs**

✅ **Consumer Behavior:**  
- Subscribes to the `order_stream` and pulls messages from the `orders` subject.
- Checks each message’s content:
  - If it contains `"fail"`, the message is published to the `order_dlq` stream and acknowledged (so it doesn’t get redelivered from the main stream).
  - If it contains `"pass"`, the message is acknowledged as successfully processed.

Example logs:

```
Received: fail Order 1
Detected failure in message. Sending to DLQ.
Message sent to DLQ and acknowledged.

Received: pass Order 3
Message processed successfully and acknowledged.
```

✅ **Key Observations:**  
- The consumer **immediately sends failed messages to the DLQ** — there’s no NAK or retry logic here.
- Messages are acknowledged whether they succeed or fail, ensuring that they aren’t redelivered to the main consumer.

---

## 📥 **DLQ Subscription Logs**

✅ **DLQ Behavior:**  
- Messages that fail processing are published to the `orders.dlq` subject and collected in the `order_dlq` stream.
- Subscribing to the DLQ allows viewing these failed messages.

Example logs:

```
nats sub orders.dlq
22:01:53 Subscribing on orders.dlq 
[#1] Received on "orders.dlq"
fail Order 17

[#2] Received on "orders.dlq"
fail Order 21
```

✅ **Key Observations:**  
- Messages like `fail Order 17` and `fail Order 21` were correctly sent to the DLQ after encountering a failure in the consumer.
- The DLQ now holds these failed messages for further investigation or reprocessing.

---

## 🔍 **Overall Flow**

1️⃣ **Producer:**  
- Publishes orders to the `order_stream` on the subject `"orders"`.  
- Messages randomly contain `"pass"` or `"fail"`.  
- Each message receives a publish acknowledgment.

2️⃣ **Consumer:**  
- Pulls messages from the `order_stream` (using durable consumer `order_consumer`).  
- Processes each message:
  - If it contains `"pass"`, it’s acknowledged and marked as processed.
  - If it contains `"fail"`, it’s published to the DLQ and acknowledged to remove it from the main stream.

3️⃣ **DLQ Stream:**  
- Collects failed messages on the subject `"orders.dlq"`.  
- Subscribing to this stream shows messages that were sent to the DLQ.

---

## 🧑‍💻 **Key Takeaways**

✅ **What’s Working:**  
- Main stream and DLQ streams are correctly set up.  
- Producer is sending both successful and failed orders.  
- Consumer immediately sends failed messages to the DLQ without retries or NAKs.  
- DLQ captures failed orders, and we  can inspect them via `nats sub orders.dlq`.

✅ **What’s Next:**  
- If we’d like to experiment with retries and NAKs, we could adjust the consumer to avoid acknowledging failed messages, allowing them to go through max redelivery attempts before hitting the DLQ.
- We could add metadata (timestamps, error reasons) to DLQ messages for better monitoring and debugging.

---
