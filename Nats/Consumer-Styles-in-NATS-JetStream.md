## Consumer Styles in NATS JetStream

NATS JetStream supports **two consumption models**:

1. **Push-Based Consumers:**  
   In this model, the server automatically “pushes” messages to the consumer’s designated subject (the deliver subject). The consumer simply subscribes to that deliver subject and receives messages as they arrive.

2. **Pull-Based Consumers:**  
   Here, the consumer explicitly requests messages from the server by “pulling” them. The consumer periodically or on-demand fetches messages from the stream.

Both models can be used depending on our use case. Push-based consumers are similar in spirit to how RabbitMQ or push-based Kafka consumers work, while pull-based consumers give we full control over when messages are retrieved—much like how a Kafka consumer might poll for new messages.

---

## Example Commands and Explanations

### 1. **Push-Based Consumer**

When we create a push consumer, we specify a delivery target. The NATS server then automatically pushes messages to that target.

#### **Creating a Push Consumer**

```bash
nats consumer add order_stream order_consumer_push --target "deliver.orders"
```

**What this command does:**

- **`order_stream`**: The stream from which messages are consumed.
- **`order_consumer_push`**: The durable consumer’s name.
- **`--target "deliver.orders"`**: Specifies the subject to which the server will push messages.  
  (This is similar to a queue in RabbitMQ where a subscriber listens on that target.)

#### **Subscribing to the Push Consumer**

After creating the consumer, we can subscribe to the delivery subject:

```bash
nats sub deliver.orders
```

**What happens:**

- When a publisher sends a message to `"orders"`, the message is stored in `order_stream`.
- The server automatically pushes the message to `"deliver.orders"`, and any subscriber on that subject receives it immediately.

---

### 2. **Pull-Based Consumer**

Pull-based consumers require the consumer to request messages. This gives we more control over the flow, especially useful when we want to pace the consumption or process messages in batches.

#### **Creating a Pull Consumer**

```bash
nats consumer add order_stream order_consumer_pull --pull --wait 2s --max-deliver 3
```

**What this command does:**

- **`order_stream`**: The stream from which messages are consumed.
- **`order_consumer_pull`**: The durable consumer’s name.
- **`--pull`**: Indicates that this is a pull-based consumer.
- **`--wait 2s`**: Sets the acknowledgment wait time to 2 seconds. If a message isn’t acknowledged within that time, it may be redelivered.
- **`--max-deliver 3`**: Limits each message to 3 delivery attempts.

#### **Fetching Messages with a Pull Consumer**

To retrieve messages, we must explicitly fetch them. For example:

```bash
nats consumer next order_stream order_consumer_pull
```

**What happens:**

- The consumer issues a fetch request.
- The server sends the next available message from `order_stream` to `order_consumer_pull`.
- our client code (or CLI) processes and then acknowledges the message.

---

## Example Flow When Publishing Data

Let’s see what happens when we publish data using these two styles:

### **Publishing a Message**

```bash
nats pub orders "pass Order 101"
```

**For a Push Consumer:**

- The message `"pass Order 101"` is stored in the stream `order_stream`.
- The NATS server automatically pushes this message to the deliver subject `"deliver.orders"`.
- Subscribers on `"deliver.orders"` receive the message immediately.

**For a Pull Consumer:**

- The message is stored in `order_stream`.
- The pull consumer must explicitly fetch the message using:
  ```bash
  nats consumer next order_stream order_consumer_pull
  ```
- Once fetched, the consumer processes the message and acknowledges it.

---

## Summary Comments

- **Push-Based Consumption:**  
  - **Pros:** Low latency delivery; server-driven push.
  - **Cons:** we must set up a delivery target; can be less controlled in terms of pacing.
  
- **Pull-Based Consumption:**  
  - **Pros:** Full control over when and how many messages to fetch; better for batch processing.
  - **Cons:** Requires explicit polling which might introduce latency if not managed properly.


---
