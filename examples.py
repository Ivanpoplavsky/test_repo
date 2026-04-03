"""
Примеры использования конвертора валют.
"""

from src.currency_converter import CurrencyConverter


def example_basic_conversion():
    """Пример 1: Базовая конвертация RUB -> VND"""
    converter = CurrencyConverter()
    
    print("\n" + "="*60)
    print("ПРИМЕР 1: Базовая конвертация")
    print("="*60)
    
    # Конвертируем 10000 рублей в донги
    converter.print_conversion(
        from_amount=10000,
        from_currency="RUB",
        to_currency="VND"
    )


def example_get_exchange_rate():
    """Пример 2: Получение обменного курса"""
    converter = CurrencyConverter()
    
    print("\n" + "="*60)
    print("ПРИМЕР 2: Получение обменного курса RUB/USD")
    print("="*60)
    
    rate = converter.get_exchange_rate("RUB", "USD")
    print(f"1 RUB = {rate:.4f} USD\n")


def example_multiple_pairs():
    """Пример 3: Конвертация нескольких пар валют"""
    converter = CurrencyConverter()
    
    print("\n" + "="*60)
    print("ПРИМЕР 3: Конвертация разных пар валют")
    print("="*60)
    
    pairs = [
        (1000, "RUB", "USD"),
        (100, "USD", "EUR"),
        (50, "GBP", "JPY"),
    ]
    
    for from_amount, from_curr, to_curr in pairs:
        try:
            result, details = converter.convert_via_crypto(
                from_amount, from_curr, to_curr
            )
            print(f"\n{from_amount} {from_curr} = {result:.2f} {to_curr}")
        except Exception as e:
            print(f"Ошибка: {from_curr} -> {to_curr}: {str(e)}")


def example_crypto_price():
    """Пример 4: Получение текущей цены крипто"""
    converter = CurrencyConverter()
    
    print("\n" + "="*60)
    print("ПРИМЕР 4: Получение цены USDT в разных валютах")
    print("="*60)
    
    currencies = ["USD", "RUB", "EUR", "VND"]
    
    for curr in currencies:
        try:
            price = converter.get_crypto_price("tether", curr)
            print(f"1 USDT = {price:.2f} {curr}")
        except Exception as e:
            print(f"Ошибка получения цены в {curr}: {str(e)}")


if __name__ == "__main__":
    example_basic_conversion()
    example_get_exchange_rate()
    example_multiple_pairs()
    example_crypto_price()
