"""
Модульные тесты для CurrencyConverter.
"""

import unittest
from unittest.mock import patch, MagicMock
from decimal import Decimal
from src.currency_converter import CurrencyConverter


class TestCurrencyConverter(unittest.TestCase):
    """Набор тестов для класса CurrencyConverter."""
    
    def setUp(self):
        """Инициализация перед каждым тестом."""
        self.converter = CurrencyConverter()
    
    @patch('requests.get')
    def test_get_crypto_price_success(self, mock_get):
        """Тест успешного получения цены крипто."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "tether": {"usd": 1.0}
        }
        mock_get.return_value = mock_response
        
        price = self.converter.get_crypto_price("tether", "usd")
        
        self.assertEqual(price, Decimal("1.0"))
    
    @patch('requests.get')
    def test_get_crypto_price_different_currencies(self, mock_get):
        """Тест получения цены в разных валютах."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "tether": {"rub": 93.5, "eur": 0.92}
        }
        mock_get.return_value = mock_response
        
        price_rub = self.converter.get_crypto_price("tether", "rub")
        self.assertEqual(price_rub, Decimal("93.5"))
    
    @patch('requests.get')
    def test_get_crypto_price_invalid_crypto(self, mock_get):
        """Тест ошибки при неверной криптовалюте."""
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        
        with self.assertRaises(ValueError) as context:
            self.converter.get_crypto_price("invalid_crypto", "usd")
        
        self.assertIn("не найдена", str(context.exception))
    
    @patch('requests.get')
    def test_get_crypto_price_empty_params(self, mock_get):
        """Тест ошибки при пустых параметрах."""
        with self.assertRaises(ValueError):
            self.converter.get_crypto_price("", "usd")
        
        with self.assertRaises(ValueError):
            self.converter.get_crypto_price("tether", "")
    
    @patch('requests.get')
    def test_convert_via_crypto_basic(self, mock_get):
        """Тест базовой конвертации RUB -> USD."""
        mock_response = MagicMock()
        mock_response.json.side_effect = [
            {"tether": {"rub": 93.5}},  # Цена USDT в RUB
            {"tether": {"usd": 1.0}}    # Цена USDT в USD
        ]
        mock_get.return_value = mock_response
        
        result, details = self.converter.convert_via_crypto(
            1000, "RUB", "USD"
        )
        
        # 1000 RUB / 93.5 = 10.695 USDT
        # 10.695 USDT * 1.0 = 10.695 USD
        self.assertAlmostEqual(float(result), 10.695, places=2)
        self.assertEqual(details['from_amount'], Decimal("1000"))
        self.assertEqual(details['to_currency'], "USD")
    
    @patch('requests.get')
    def test_convert_via_crypto_zero_amount(self, mock_get):
        """Тест ошибки при нулевой сумме."""
        with self.assertRaises(ValueError) as context:
            self.converter.convert_via_crypto(0, "RUB", "USD")
        
        self.assertIn("больше нуля", str(context.exception))
    
    @patch('requests.get')
    def test_convert_via_crypto_negative_amount(self, mock_get):
        """Тест ошибки при отрицательной сумме."""
        with self.assertRaises(ValueError):
            self.converter.convert_via_crypto(-100, "RUB", "USD")
    
    @patch('requests.get')
    def test_convert_via_crypto_case_insensitive(self, mock_get):
        """Тест что коды валют обрабатываются регистронезависимо."""
        mock_response = MagicMock()
        mock_response.json.side_effect = [
            {"tether": {"rub": 93.5}},
            {"tether": {"usd": 1.0}}
        ]
        mock_get.return_value = mock_response
        
        # Разные комбинации регистра
        result1, _ = self.converter.convert_via_crypto(100, "rub", "usd")
        result2, _ = self.converter.convert_via_crypto(100, "RUB", "USD")
        result3, _ = self.converter.convert_via_crypto(100, "Rub", "UsD")
        
        # Все должны дать одинаковый результат
        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)
    
    @patch('requests.get')
    def test_get_exchange_rate(self, mock_get):
        """Тест получения обменного курса."""
        mock_response = MagicMock()
        mock_response.json.side_effect = [
            {"tether": {"rub": 93.5}},
            {"tether": {"usd": 1.0}}
        ]
        mock_get.return_value = mock_response
        
        rate = self.converter.get_exchange_rate("RUB", "USD")
        
        # 1 RUB = (1 / 93.5) * 1.0 USD
        expected = Decimal("1") / Decimal("93.5")
        self.assertAlmostEqual(float(rate), float(expected), places=4)
    
    @patch('requests.get')
    def test_get_fiat_currencies_cached(self, mock_get):
        """Тест что результат кэшируется."""
        currencies = {"usd": "usd", "eur": "eur", "rub": "rub"}
        
        mock_response = MagicMock()
        mock_response.json.return_value = list(currencies.keys())
        mock_get.return_value = mock_response
        
        # Первый вызов - идет в API
        result1 = self.converter.get_fiat_currencies()
        call_count_first = mock_get.call_count
        
        # Второй вызов - должен быть кэшширован
        result2 = self.converter.get_fiat_currencies()
        call_count_second = mock_get.call_count
        
        # Количество вызовов не должно измениться
        self.assertEqual(call_count_first, call_count_second)
        self.assertEqual(result1, result2)
    
    @patch('requests.get')
    def test_conversion_two_step_calculation(self, mock_get):
        """Тест правильности двухшагового расчета."""
        mock_response = MagicMock()
        mock_response.json.side_effect = [
            {"tether": {"rub": 80.0}},   # 1 USDT = 80 RUB
            {"tether": {"vnd": 24000.0}} # 1 USDT = 24000 VND
        ]
        mock_get.return_value = mock_response
        
        result, details = self.converter.convert_via_crypto(
            8000, "RUB", "VND"
        )
        
        # Шаг 1: 8000 RUB / 80 = 100 USDT
        expected_crypto = Decimal("8000") / Decimal("80")
        self.assertEqual(details['crypto_amount'], expected_crypto)
        
        # Шаг 2: 100 USDT * 24000 = 2,400,000 VND
        expected_result = expected_crypto * Decimal("24000")
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
