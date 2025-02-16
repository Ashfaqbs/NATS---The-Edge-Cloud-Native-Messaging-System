- open a powershell:

resource:
```
 https://github.com/nats-io/natscli?tab=readme-ov-file
 https://scoop.sh/
```
- install scoop:

PS C:\Users\ashfa> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Execution Policy Change
The execution policy helps protect you from scripts that you do not trust. Changing the execution policy might expose
you to the security risks described in the about_Execution_Policies help topic at
https:/go.microsoft.com/fwlink/?LinkID=135170. Do you want to change the execution policy?
[Y] Yes  [A] Yes to All  [N] No  [L] No to All  [S] Suspend  [?] Help (default is "N"): y
PS C:\Users\ashfa> Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
Initializing...
Downloading...
Creating shim...
Adding ~\scoop\shims to your path.
Scoop was installed successfully!

- install natscli:
```
PS C:\Users\ashfa> scoop bucket add extras
Checking repo... OK
The extras bucket was added successfully.
PS C:\Users\ashfa> scoop install extras/natscli
Installing 'natscli' (0.1.6) [64bit] from 'extras' bucket
nats-0.1.6-windows-amd64.zip (9.3 MB) [=======================================================================] 100%
Checking hash of nats-0.1.6-windows-amd64.zip ... ok.
Extracting nats-0.1.6-windows-amd64.zip ... done.
Linking ~\scoop\apps\natscli\current => ~\scoop\apps\natscli\0.1.6
Creating shim for 'nats'.
'natscli' (0.1.6) was installed successfully!
```

- run natscli example:

```
PS C:\Users\ashfa> nats stream add mystream --subjects "mymessages"
? Storage memory
? Replication [? for help] (1) 1

? Replication 1
? Retention Policy Limits
? Discard Policy Old
? Stream Messages Limit [? for help] (-1)

? Stream Messages Limit -1
? Per Subject Messages Limit [? for help] (-1) -1

? Per Subject Messages Limit -1
? Total Stream Size [? for help] (-1) -1

? Total Stream Size -1
? Message TTL -1
? Max Message Size -1
? Allow purging subjects or the entire stream No
Stream mystream was created the entire stream (Y/n) n

Information for Stream mystream created 2025-02-12 20:22:32

              Subjects: mymessages
              Replicas: 1
               Storage: Memory

Options:

             Retention: Limits
       Acknowledgments: true
        Discard Policy: Old
      Duplicate Window: 2m0s
            Direct Get: true
     Allows Msg Delete: true
          Allows Purge: false
        Allows Rollups: false

Limits:

      Maximum Messages: unlimited
   Maximum Per Subject: unlimited
         Maximum Bytes: unlimited
           Maximum Age: unlimited
  Maximum Message Size: unlimited
     Maximum Consumers: unlimited

State:

              Messages: 0
                 Bytes: 0 B
        First Sequence: 0
         Last Sequence: 0
      Active Consumers: 0
PS C:\Users\ashfa> nats pub mymessages "Hello, NATS JetStream!"
20:22:44 Published 22 bytes to "mymessages"
PS C:\Users\ashfa> nats consumer add mystream myconsumer
? Delivery target (empty for Pull Consumers)
? Start policy (all, new, last, subject, 1h, msg sequence) all
? Acknowledgment policy all
? Replay policy instant
? Filter Stream by subjects (blank for all) [? for help]

? Filter Stream by subjects (blank for all)
? Maximum Allowed Deliveries -1
? Add a Retry Backoff Policy Yes
? Backoff policy none
Information for Consumer mystream > myconsumer created 2025-02-12T20:23:11+05:30

Configuration:

                    Name: myconsumer
               Pull Mode: true
          Deliver Policy: All
              Ack Policy: All
                Ack Wait: 30.00s
           Replay Policy: Instant
         Max Ack Pending: 1,000
       Max Waiting Pulls: 512

State:

  Last Delivered Message: Consumer sequence: 0 Stream sequence: 0
    Acknowledgment Floor: Consumer sequence: 0 Stream sequence: 0
        Outstanding Acks: 0 out of maximum 1,000
    Redelivered Messages: 0
    Unprocessed Messages: 1
           Waiting Pulls: 0 of maximum 512
PS C:\Users\ashfa> nats consumer next mystream myconsumer
[20:23:17] subj: mymessages / tries: 1 / cons seq: 1 / str seq: 1 / pending: 0

Hello, NATS JetStream!

Acknowledged message

PS C:\Users\ashfa>
```

















To manage NATS JetStream via the command-line interface (CLI), we'll use the `nats` CLI tool. This utility allows us to interact with and manage NATS, including full JetStream management.

**Installation:**

For detailed installation instructions, refer to the [NATS CLI GitHub repository](https://github.com/nats-io/natscli).

**Creating a Stream:**

A stream in JetStream is a storage unit that retains messages for subjects. To create a stream named `mystream` that stores messages sent to the subject `mymessages`, we can use the following command:

```bash
nats stream add mystream --subjects "mymessages"
```

This command sets up a stream named `mystream` that listens to the subject `mymessages`.

**Publishing a Message:**

To publish a message to the `mymessages` subject, execute:

```bash
nats pub mymessages "Hello, NATS JetStream!"
```

This command sends the message "Hello, NATS JetStream!" to the `mymessages` subject.

**Subscribing to a Stream:**

To receive messages from a stream, we need to create a consumer. For a ``pull-based`` consumer named `myconsumer` on the `mystream` stream, run:

```bash
nats consumer add mystream myconsumer
```

After creating the consumer, we can pull messages using:

```bash
nats consumer next mystream myconsumer
```

This command retrieves messages from the `mystream` stream using the `myconsumer` consumer.

For more detailed information and advanced configurations, refer to the [NATS JetStream Walkthrough](https://docs.nats.io/nats-concepts/jetstream/js_walkthrough).
