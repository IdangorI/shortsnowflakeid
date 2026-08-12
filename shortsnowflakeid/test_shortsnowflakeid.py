import unittest
import time
from shortsnowflakeid.main import ShortSnowflakeID

class TestShortSnowflakeID(unittest.TestCase):
    def setUp(self):
        self.generator = ShortSnowflakeID(node_id=1)

    def test_fixed_length(self):
        for _ in range(100):
            short_id = self.generator.random()
            self.assertEqual(len(short_id), self.generator.fixed_length)

    def test_encode_decode_roundtrip(self):
        original_int = self.generator.random_int()
        encoded = self.generator.encode(original_int)
        decoded_int = self.generator.decode(encoded)
        
        self.assertEqual(original_int, decoded_int)

    def test_short_id_decode_roundtrip(self):
        short_id = self.generator.random()
        decoded_int = self.generator.decode(short_id)
        re_encoded = self.generator.encode(decoded_int)
        
        self.assertEqual(short_id, re_encoded)

    def test_lexicographical_sorting(self):
        ids = []
        for _ in range(50):
            ids.append(self.generator.random())
            time.sleep(0.001)

        sorted_ids = sorted(ids)
        
        self.assertEqual(ids, sorted_ids)

    def test_timestamp_decryption(self):
        before_time = int(time.time() * 1000)
        short_id = self.generator.random()
        full_id = self.generator.decode(short_id)
        after_time = int(time.time() * 1000)

        time_from_str = self.generator.decode_timestamp_ms(short_id)
        time_from_int = self.generator.decode_timestamp_ms_int(full_id)

        self.assertEqual(time_from_str, time_from_int)
        self.assertTrue(before_time <= time_from_str <= after_time)

    def test_sequence_increment(self):
        id1 = self.generator.random_int()
        id2 = self.generator.random_int()
        
        self.assertGreater(id2, id1)

    def test_invalid_character_raises_error(self):
        invalid_id = "1" * self.generator.fixed_length
        
        with self.assertRaises(ValueError):
            self.generator.decode(invalid_id)

    def test_node_id_masking(self):
        gen_large_node = ShortSnowflakeID(node_id=2048)

        self.assertEqual(gen_large_node.node_id, 0)


if __name__ == "__main__":
    unittest.main()