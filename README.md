# Short Snowflake ID

A lightweight Python library that bridges the gap between distributed [Snowflake IDs](https://en.wikipedia.org/wiki/Snowflake_ID) and clean, compact, time-sortable strings.

## Overview

Standard database auto-increment counters leak business data (like total record counts) and look clumsy in web links. On the other hand, traditional random UUIDs solve privacy issues but wreck database indexing because they are completely chaotic and un-sortable.

**ShortSnowflakeID** combines the best of both worlds:
1. **Distributed & Monotonic:** Generates 63-bit integers containing a millisecond timestamp, a node ID, and an inner sequence counter.
2. **Human & URL-Friendly:** Translates those numbers into fixed-length strings using a custom, unambiguous alphabet (stripping out easily confused glyphs like `l`, `1`, `I`, `O`, and `0`).
3. **Chronologically Sorted:** Because the underlying numbers strictly increase over time, the resulting strings sort naturally in databases just like standard numbers.

## Key Features

- **Time-Sortable:** Ideal for database primary keys, cursors, and chronological feeds.
- **Cluster-Ready:** Safely run across multiple servers or worker threads using unique `node_id` configurations.
- **Embedded Metadata:** Extract the exact creation timestamp down to the millisecond straight from the ID, without hitting the database.
- **No Heavy Dependencies:** Pure, clean Python implementation.

## Installation

Ensure you are running **Python 3.6+** and include the module in your project source tree.

## Usage

Just import it in your project like so:

```python
>>> import shortsnowflakeid
```

### Generating a Short ID

```python
>>> shortsnowflakeid.random()
'3e26HbYeqZh'
```

### Getting the Raw Integer

If your database prefers working with numerical IDs under the hood:
```python
>>> shortsnowflakeid.random_int()
590696153977196544
```

### Encoding and Decoding

Seamlessly convert back and forth between raw integers and concise strings:

```python
>>> s = shortsnowflakeid.encode(590696153977196544)
>>> s
'3e27EC89Wjx'
>>> shortsnowflakeid.decode(s) == 590696153977196544
True
```

### Reading the Timestamp

Retrieve the precise creation moment (in Unix milliseconds) from any short string or raw integer:

```python
>>> shortsnowflakeid.decode_timestamp_ms(s)
1786540537712
```

### Customization

You can easily tailor the generator to your needs by adjusting the node ID, custom epoch, or alphabet set during initialization:

```python
custom_generator = shortsnowflakeid.ShortSnowflakeID(
    node_id=3,
    epoch=1645707600000,
    alphabet="23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
)
```

## License

```shortsnowflakeid``` is distributed under the BSD license.