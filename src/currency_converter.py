"""
Конвертор валют через криптовалюту (USDT).

Позволяет обменивать одну валюту на другую через промежуточную криптовалюту.
Например: RUB -> USDT -> VND
"""

import requests
from typing import Dict, Optional, Tuple
from decimal import Decimal


class CurrencyConverter:
    """
    Конвертор валют использующий крипто-мост (USDT).
    
    Получает текущие курсы от CoinGecko API и вычисляет обменные курсы
    через промежуточную криптовалюту.
    """
    
    COINGECKO_API = "https://api.coingecko.com/api/v3"
    USDT_ID = "tether"  # CoinGecko ID для USDT
    
    def __init__(self):
        """Инициализирует конвертор и загружает доступные валюты."""
        self._cache_fiat_currencies = None
    
    def get_fiat_currencies(self) -> Dict[str, str]:
        """
        Получает список поддерживаемых фиатных валют.
        
        Returns:
            Dict[str, str]: Словарь валют {код: название}
            
        Raises:
            requests.RequestException: При ошибке подключения к API
        """
        if self._cache_fiat_currencies is not None:
            return self._cache_fiat_currencies
            
        try:
            response = requests.get(
                f"{self.COINGECKO_API}/simple/supported_vs_currencies",
                timeout=10
            )
            response.raise_for_status()
            currencies = response.json()
            
            # Преобразуем в словарь {код: код}
            self._cache_fiat_currencies = {code: code.upper() for code in currencies}
            return self._cache_fiat_currencies
            
        except requests.RequestException as e:
            raise requests.RequestException(
                f"Ошибка при получении списка валют: {str(e)}"
            ) from e
    
    def get_crypto_price(self, crypto_id: str, vs_currency: str) -> Decimal:
        """
        Получает цену криптовалюты в указанной фиатной валюте.
        
        Args:
            crypto_id: ID криптовалюты на CoinGecko (например, 'bitcoin')
            vs_currency: Код валюты для получения цены (например, 'usd')
            
        Returns:
            Decimal: Текущая цена 1 единицы крипто в указанной валюте
            
        Raises:
            requests.RequestException: При ошибке подключения к API
            ValueError: При неверных параметрах
        """
        if not crypto_id or not vs_currency:
            raise ValueError("crypto_id и vs_currency не могут быть пустыми")
            
        try:
            response = requests.get(
                f"{self.COINGECKO_API}/simple/price",
                params={
                    "ids": crypto_id.lower(),
                    "vs_currencies": vs_currency.lower()
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if not data or crypto_id.lower() not in data:
                raise ValueError(f"Криптовалюта '{crypto_id}' не найдена")
                
            price = data[crypto_id.lower()].get(vs_currency.lower())
            if price is None:
                raise ValueError(
                    f"Цена для {crypto_id} в {vs_currency} не доступна"
                )
                
            return Decimal(str(price))
            
        except requests.RequestException as e:
            raise requests.RequestException(
                f"Ошибка при получении курса {crypto_id}: {str(e)}"
            ) from e
    
    def convert_via_crypto(
        self,
        from_amount: float,
        from_currency: str,
        to_currency: str,
        crypto_id: str = USDT_ID
    ) -> Tuple[Decimal, Dict[str, Decimal]]:
        """
        Конвертирует сумму из одной валюты в другую через криптовалюту.
        
        Процесс:
        1. from_currency -> crypto (продаём фиатную валюту за крипто)
        2. crypto -> to_currency (продаём крипто за целевую валюту)
        
        Args:
            from_amount: Сумма для конвертации
            from_currency: Исходная валюта (код, например 'RUB')
            to_currency: Целевая валюта (код, например 'VND')
            crypto_id: ID криптовалюты для обмена (по умолчанию 'tether' для USDT)
            
        Returns:
            Tuple[Decimal, Dict]: (Итоговая сумма, Детали обмена)
            
        Raises:
            ValueError: При неверных параметрах
            requests.RequestException: При ошибке подключения к API
        """
        if from_amount <= 0:
            raise ValueError("Сумма должна быть больше нуля")
            
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        # Получаем цены крипто в обеих валютах
        price_in_from = self.get_crypto_price(crypto_id, from_currency)
        price_in_to = self.get_crypto_price(crypto_id, to_currency)
        
        # Вычисляем количество крипто которое получим
        crypto_amount = Decimal(str(from_amount)) / price_in_from
        
        # Конвертируем крипто в целевую валюту
        final_amount = crypto_amount * price_in_to
        
        details = {
            "from_amount": Decimal(str(from_amount)),
            "from_currency": from_currency,
            "crypto_id": crypto_id.upper(),
            "crypto_amount": crypto_amount,
            "crypto_price_in_from": price_in_from,
            "crypto_price_in_to": price_in_to,
            "to_amount": final_amount,
            "to_currency": to_currency,
        }
        
        return final_amount, details
    
    def get_exchange_rate(
        self,
        from_currency: str,
        to_currency: str,
        crypto_id: str = USDT_ID
    ) -> Decimal:
        """
        Получает обменный курс между двумя валютами через крипто.
        
        Args:
            from_currency: Исходная валюта
            to_currency: Целевая валюта
            crypto_id: ID криптовалюты для обмена
            
        Returns:
            Decimal: Сколько единиц to_currency получим за 1 единицу from_currency
        """
        final_amount, _ = self.convert_via_crypto(
            1.0, from_currency, to_currency, crypto_id
        )
        return final_amount
    
    def print_conversion(
        self,
        from_amount: float,
        from_currency: str,
        to_currency: str,
        crypto_id: str = USDT_ID
    ) -> None:
        """
        Красиво выводит конвертацию в консоль.
        
        Args:
            from_amount: Сумма для конвертации
            from_currency: Исходная валюта
            to_currency: Целевая валюта
            crypto_id: ID криптовалюты
        """
        try:
            result, details = self.convert_via_crypto(
                from_amount, from_currency, to_currency, crypto_id
            )
            
            print(f"\n{'='*60}")
            print(f"Конвертация валют через крипто-мост")
            print(f"{'='*60}")
            print(f"Исходная сумма:      {details['from_amount']} {details['from_currency']}")
            print(f"\nШаг 1: {details['from_currency']} -> {details['crypto_id']}")
            print(f"  Курс: 1 {details['crypto_id']} = {details['crypto_price_in_from']:.2f} {details['from_currency']}")
            print(f"  Получим крипто: {details['crypto_amount']:.8f} {details['crypto_id']}")
            print(f"\nШаг 2: {details['crypto_id']} -> {details['to_currency']}")
            print(f"  Курс: 1 {details['crypto_id']} = {details['crypto_price_in_to']:.2f} {details['to_currency']}")
            print(f"\nИтоговая сумма:      {result:.2f} {details['to_currency']}")
            print(f"{'='*60}\n")
            
        except Exception as e:
            print(f"Ошибка при конвертации: {str(e)}")
