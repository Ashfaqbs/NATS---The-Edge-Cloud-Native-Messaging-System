import asyncio
from nats.aio.client import Client as NATS

async def run_consumer():
    # Connect to NATS server
    nc = NATS()
    await nc.connect("localhost:4222")
    
    # Obtain a JetStream context to get JetStream APIs for publish/subscribe
    js = nc.jetstream()
    
    # Use pull_subscribe for pull-based consumption.
    sub = await js.pull_subscribe("mymessages", durable="myconsumer")
    
    while True:
        try:
            # Fetch one message with a timeout (in seconds)
            msgs = await sub.fetch(1, timeout=5)
            for msg in msgs:
                print(f"Received: {msg.data.decode()}")
                await msg.ack()
        except Exception as e:
            print("No messages or error fetching messages:", e)
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(run_consumer())
