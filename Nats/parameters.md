When using the NATS CLI to add streams and consumers, we're prompted to configure various parameters that define their behavior. Below is a breakdown of the prompts for each command, including the questions asked, default values, valid input ranges, and the impact of these configurations.

**1. Adding a Stream: `nats stream add mystream --subjects "mymessages"`**

*Prompts and Configurations:*

- **Storage**: Determines where the stream's data is stored.
  - *Prompt*: `Storage`
  - *Default*: `file`
  - *Options*: `file`, `memory`
  - *Impact*: `file` stores data on disk, providing persistence across restarts; `memory` keeps data in RAM, offering faster access but data is lost on server restarts.

- **Replication**: Sets the number of replicas for the stream.
  - *Prompt*: `Replication`
  - *Default*: `1`
  - *Range*: `1` to the number of available nodes
  - *Impact*: Higher replication increases data redundancy and fault tolerance but consumes more resources.

- **Retention Policy**: Defines how messages are retained.
  - *Prompt*: `Retention Policy`
  - *Default*: `Limits`
  - *Options*: `Limits`, `Interest`, `Work Queue`
  - *Impact*:
    - `Limits`: Retains messages based on specified limits (e.g., message count, size).
    - `Interest`: Retains messages only if there are active consumers.
    - `Work Queue`: Retains messages until they are acknowledged by a consumer.

- **Discard Policy**: Specifies what happens when the stream reaches its limits.
  - *Prompt*: `Discard Policy`
  - *Default*: `Old`
  - *Options*: `Old`, `New`
  - *Impact*:
    - `Old`: Discards oldest messages when limits are reached.
    - `New`: Rejects new messages when limits are reached.

- **Stream Messages Limit**: Sets the maximum number of messages the stream can hold.
  - *Prompt*: `Stream Messages Limit`
  - *Default*: `-1` (unlimited)
  - *Range*: `-1` (unlimited) or any positive integer
  - *Impact*: Limits the number of messages; older messages are discarded based on the discard policy when the limit is reached.

- **Per Subject Messages Limit**: Limits the number of messages per subject.
  - *Prompt*: `Per Subject Messages Limit`
  - *Default*: `-1` (unlimited)
  - *Range*: `-1` (unlimited) or any positive integer
  - *Impact*: Controls the number of messages retained for each subject within the stream.

- **Total Stream Size**: Specifies the maximum storage size for the stream.
  - *Prompt*: `Total Stream Size`
  - *Default*: `-1` (unlimited)
  - *Range*: `-1` (unlimited) or any positive integer (in bytes)
  - *Impact*: Limits the total storage used by the stream; older messages are discarded based on the discard policy when the limit is reached.

- **Message TTL**: Sets the time-to-live for messages.
  - *Prompt*: `Message TTL`
  - *Default*: `-1` (no expiration)
  - *Range*: `-1` (no expiration) or any positive integer (in nanoseconds)
  - *Impact*: Messages older than the specified TTL are automatically removed from the stream.

- **Max Message Size**: Defines the maximum size of individual messages.
  - *Prompt*: `Max Message Size`
  - *Default*: `-1` (unlimited)
  - *Range*: `-1` (unlimited) or any positive integer (in bytes)
  - *Impact*: Messages exceeding this size are rejected.

- **Allow Purging**: Indicates if manual purging of the stream is permitted.
  - *Prompt*: `Allow purging subjects or the entire stream`
  - *Default*: `No`
  - *Options*: `Yes`, `No`
  - *Impact*: If enabled, allows manual deletion of messages or entire subjects from the stream.

*Example Configuration:*

If we set `Storage` to `memory`, `Replication` to `2`, `Retention Policy` to `Interest`, and `Stream Messages Limit` to `1000`, the stream will:

- Store data in memory.
- Replicate data across 2 nodes.
- Retain messages only if there are active consumers.
- Hold up to 1,000 messages, discarding the oldest when 