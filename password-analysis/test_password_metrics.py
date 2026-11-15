import unittest

from src.password_metrics import alphabet_estimate_bits, benchmark, shannon_entropy_bits


class PasswordMetricsTests(unittest.TestCase):
    def test_empty_and_repeated_values(self):
        self.assertEqual(shannon_entropy_bits(""), 0.0)
        self.assertEqual(shannon_entropy_bits("aaaa"), 0.0)

    def test_uniform_two_character_sample(self):
        self.assertAlmostEqual(shannon_entropy_bits("abab"), 1.0)

    def test_alphabet_estimate(self):
        self.assertGreater(alphabet_estimate_bits("Ab3!"), 0)
        self.assertEqual(alphabet_estimate_bits(""), 0.0)

    def test_benchmark_returns_metrics_not_secret(self):
        result = benchmark("synthetic-demo", scrypt_n=2**10)
        self.assertIn("scrypt_ms", result)
        self.assertNotIn("password", result)


if __name__ == "__main__":
    unittest.main()
