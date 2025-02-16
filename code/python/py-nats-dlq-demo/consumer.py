import asyncio
from nats.aio.client import Client as NATS

async def run_consumer():
    # Connect to the NATS server
    nc = NATS()
    await nc.connect("localhost:4222")
    
    # Create a JetStream context
    js = nc.jetstream()
    
    # Create a pull-based durable consumer on the "orders" subject.
    # "order_consumer" is the durable consumer name.
    sub = await js.pull_subscribe("orders", durable="order_consumer")
    
    while True:
        try:
            # Fetch one message at a time with a timeout of 5 seconds.
            msgs = await sub.fetch(1, timeout=5)
            for msg in msgs:
                # Decode the message data into a string.
                data = msg.data.decode()
                print(f"Received: {data}")
                
                # Check message content:
                # If the message contains "fail", simulate a failure and send it to the DLQ.
                if "fail" in data.lower():
                    print("Detected failure in message. Sending to DLQ.")
                    # Publish the failed message to the DLQ stream on subject "orders.dlq"
                    await js.publish("orders.dlq", msg.data)
                    # Acknowledge the message so it is removed from the main stream.
                    await msg.ack()
                    print("Message sent to DLQ and acknowledged.")
                else:
                    # For a "pass" message, process and acknowledge it.
                    await msg.ack()
                    print("Message processed successfully and acknowledged.")
        except Exception as e:
            # Handle exceptions such as timeouts (when no messages are fetched)
            print("No messages fetched or an error occurred:", e)
        
        await asyncio.sleep(1)  # Short delay before fetching the next message

if __name__ == '__main__':
    asyncio.run(run_consumer())
