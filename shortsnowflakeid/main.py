import time

DEFAULT_NODE_ID = 1
DEFAULT_EPOCH = 1645707600000 # Thursday, February 24, 2022 at 5:00:00 AM UTC-08:00
DEFAULT_ALPHABET = "23456789" "ABCDEFGHJKLMNPQRSTUVWXYZ" "abcdefghijkmnopqrstuvwxyz"

class ShortSnowflakeID:
    def __init__(self, node_id: int = DEFAULT_NODE_ID, epoch: int = DEFAULT_EPOCH, alphabet: str = DEFAULT_ALPHABET) -> None:
        self.node_id = node_id & 0x3FF
        self.epoch = epoch
        self.sequence = 0
        self.last_timestamp = -1
        self.alphabet = alphabet
        self.base = len(alphabet)
        
        max_snowflake = (1 << 63) - 1
        self.fixed_length = len(self._encode_raw(max_snowflake))

    def _current_timestamp(self) -> int:
        return int(time.time() * 1000)

    def _encode_raw(self, num: int) -> str:
            if num == 0:
                return self.alphabet[0]
            chars = []
            while num > 0:
                num, rem = divmod(num, self.base)
                chars.append(self.alphabet[rem])
            return "".join(reversed(chars))

    def random_int(self) -> int:
        """Generating a Standard SnowflakeID"""
        timestamp = self._current_timestamp()

        if timestamp < self.last_timestamp:
            raise ValueError("Clock moved backwards!")

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 0xFFF
            if self.sequence == 0:
                while timestamp <= self.last_timestamp:
                    timestamp = self._current_timestamp()
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        return (
            ((timestamp - self.epoch) << 22)
            | (self.node_id << 12)
            | self.sequence
        )

    def random(self) -> str:
        """Generating a Short SnowflakeID"""
        return self.encode(self.random_int())

    def encode(self, num: int) -> str:
        """Converting a number to a fixed-length string (depends on the alphabet)"""
        encoded = self._encode_raw(num)
        return encoded.rjust(self.fixed_length, self.alphabet[0])

    def decode(self, code: str) -> int:
        """Decoding a short id back into a full id"""
        num = 0
        for char in code:
            num = num * self.base + self.alphabet.index(char)
        return num
    def decode_timestamp_ms(self, short_id: str) -> int:
        """Getting a timestamp in milliseconds using a short ID"""
        snowflake_int = self.decode(short_id)
        timestamp_ms = (snowflake_int >> 22) + self.epoch
        return timestamp_ms
    def decode_timestamp_ms_int(self, full_id: int) -> int:
        """Getting a timestamp in milliseconds using a full ID"""
        timestamp_ms = (full_id >> 22) + self.epoch
        return timestamp_ms

_global_instance = ShortSnowflakeID()
random = _global_instance.random
random_int = _global_instance.random_int
encode = _global_instance.encode
decode = _global_instance.decode
decode_timestamp_ms = _global_instance.decode_timestamp_ms
decode_timestamp_ms_int = _global_instance.decode_timestamp_ms_int