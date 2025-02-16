import asyncio
import random
from nats.aio.client import Client as NATS

async def run_producer():
    # Create a connection to the NATS server
    nc = NATS()
    await nc.connect("localhost:4222")
    
    # Create a JetStream context to interact with streams
    js = nc.jetstream()
    
    order_number = 1  # Initialize order counter
    while True:
        # Randomly decide whether to send a "pass" or "fail" message
        if random.choice([True, False]):
            message = f"pass Order {order_number}"
        else:
            message = f"fail Order {order_number}"
        
        # Publish the message to the "orders" subject in the main stream
        ack = await js.publish("orders", message.encode())
        print(f"Published: {message} (Ack: {ack})")
        
        order_number += 1  # Increment order counter
        await asyncio.sleep(1)  # Wait for 1 second before sending the next message

if __name__ == '__main__':
    asyncio.run(run_producer())
