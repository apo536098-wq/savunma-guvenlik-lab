import unittest

from src.analyze_binary import inspect_elf, inspect_pe, printable_strings


class BinaryAnalyzerTests(unittest.TestCase):
    def test_minimal_elf64_little_endian(self):
        data = bytearray(64)
        data[:6] = b"\x7fELF\x02\x01"
        data[18:20] = (62).to_bytes(2, "little")
        data[24:32] = (0x401000).to_bytes(8, "little")
        result = inspect_elf(bytes(data))
        self.assertEqual(result["class"], 64)
        self.assertEqual(result["machine_id"], 62)
        self.assertEqual(result["entry_point"], 0x401000)

    def test_minimal_pe(self):
        data = bytearray(0x80 + 24)
        data[:2] = b"MZ"
        data[0x3C:0x40] = (0x80).to_bytes(4, "little")
        data[0x80:0x84] = b"PE\0\0"
        data[0x84:0x86] = (0x8664).to_bytes(2, "little")
        data[0x86:0x88] = (3).to_bytes(2, "little")
        self.assertEqual(inspect_pe(bytes(data))["section_count"], 3)

    def test_printable_strings(self):
        self.assertEqual(printable_strings(b"\x00hello\x00xy"), ["hello"])

    def test_rejects_bad_signatures(self):
        with self.assertRaises(ValueError):
            inspect_elf(b"not elf")
        with self.assertRaises(ValueError):
            inspect_pe(b"MZ" + bytes(100))


if __name__ == "__main__":
    unittest.main()
