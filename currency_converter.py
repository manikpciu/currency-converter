# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
class Logger:
    """
    Responsible for logging every currency conversion.
    Associated with CurrencyConverter — NOT composed inside it.
    CurrencyConverter receives a Logger object from outside (Association).
    """

    def log(self, user: str, amount: float, result: str) -> None:
        """Log a conversion record to the console."""
        print(f"\n📋 [LOG] User: {user} | Amount: {amount} | Result: {result}")


# ─────────────────────────────────────────────
#  CurrencyConverter Class
# ─────────────────────────────────────────────
class CurrencyConverter:
    """
    Converts currencies using mock exchange rates.

    Class Attribute  : exchange_rates  — stores all currency exchange rates
    Instance Attrs   : amount, from_currency, to_currency
    Instance Method  : convert()       — performs the conversion
    Class Method     : update_rate()   — updates an exchange rate
    Static Method    : is_valid_code() — validates a currency code
    """

    # ── Class Attribute: shared across ALL instances ──────────
    exchange_rates = {
        "USD": 1.0,       # Base currency
        "BDT": 110.50,    # Bangladeshi Taka
        "EUR": 0.92,      # Euro
        "GBP": 0.79,      # British Pound
        "JPY": 149.50,    # Japanese Yen
        "INR": 83.12,     # Indian Rupee
        "CAD": 1.36,      # Canadian Dollar
        "AUD": 1.53,      # Australian Dollar
        "SAR": 3.75,      # Saudi Riyal
        "AED": 3.67,      # UAE Dirham
    }

    # ── __init__: sets instance attributes ───────────────────
    def __init__(self, amount: float, from_currency: str, to_currency: str):
        self.amount        = amount
        self.from_currency = from_currency.upper()
        self.to_currency   = to_currency.upper()

    # ── Instance Method: performs conversion ─────────────────
    def convert(self) -> float | None:
        """Convert amount from from_currency to to_currency."""
        if not CurrencyConverter.is_valid_code(self.from_currency):
            print(f"❌ Invalid currency code: {self.from_currency}")
            return None
        if not CurrencyConverter.is_valid_code(self.to_currency):
            print(f"❌ Invalid currency code: {self.to_currency}")
            return None

        # Convert to USD first (base), then to target currency
        amount_in_usd  = self.amount / CurrencyConverter.exchange_rates[self.from_currency]
        converted      = amount_in_usd * CurrencyConverter.exchange_rates[self.to_currency]
        return round(converted, 4)

    # ── Class Method: updates exchange rate ──────────────────
    @classmethod
    def update_rate(cls, currency_code: str, new_rate: float) -> None:
        """Update the exchange rate for a given currency code."""
        code = currency_code.upper()
        if cls.is_valid_code(code):
            cls.exchange_rates[code] = new_rate
            print(f"✅ Rate updated: 1 USD = {new_rate} {code}")
        else:
            print(f"❌ Cannot update — unknown currency code: {code}")

    # ── Static Method: validates currency code ───────────────
    @staticmethod
    def is_valid_code(code: str) -> bool:
        """Return True if the currency code exists in exchange_rates."""
        return code.upper() in CurrencyConverter.exchange_rates


# ─────────────────────────────────────────────
#  Helper: display supported currencies
# ─────────────────────────────────────────────
def show_supported_currencies() -> None:
    print("\n💱 Supported Currencies:")
    print("─" * 30)
    for code, rate in CurrencyConverter.exchange_rates.items():
        print(f"   {code:>4}  →  1 USD = {rate}")
    print("─" * 30)


# ─────────────────────────────────────────────
#  Main CLI Loop
# ─────────────────────────────────────────────
def main():
    print("=" * 50)
    print("   💰 Currency Converter CLI App")
    print("   Python OOP — Module 4 Project")
    print("=" * 50)

    # ── Create Logger object OUTSIDE CurrencyConverter (Association) ──
    logger = Logger()

    # ── Ask for user name ─────────────────────────────────────
    user_name = input("\n👤 Enter your name: ").strip() or "Anonymous"

    while True:
        print("\n─── MENU ───────────────────────────────")
        print("  1. Convert Currency")
        print("  2. Update Exchange Rate")
        print("  3. Show Supported Currencies")
        print("  4. Exit")
        print("────────────────────────────────────────")

        choice = input("Select option (1-4): ").strip()

        # ── Option 1: Convert ─────────────────────────────────
        if choice == "1":
            show_supported_currencies()
            try:
                amount        = float(input("\n💵 Enter amount      : "))
                from_currency = input("🔤 From currency code: ").strip().upper()
                to_currency   = input("🔤 To   currency code: ").strip().upper()
            except ValueError:
                print("❌ Invalid amount. Please enter a number.")
                continue

            # Instantiate CurrencyConverter
            converter = CurrencyConverter(amount, from_currency, to_currency)

            # Pass logger to convert workflow (Association — not inside the class)
            result = converter.convert()

            if result is not None:
                result_str = (
                    f"{amount} {from_currency} = {result} {to_currency}"
                )
                print(f"\n✅ {result_str}")
                # Use logger (associated object) to record the conversion
                logger.log(user_name, amount, result_str)

        # ── Option 2: Update Rate ─────────────────────────────
        elif choice == "2":
            code = input("Enter currency code to update: ").strip()
            try:
                new_rate = float(input(f"Enter new rate for {code.upper()} (vs USD): "))
                CurrencyConverter.update_rate(code, new_rate)
            except ValueError:
                print("❌ Invalid rate value.")

        # ── Option 3: Show Currencies ─────────────────────────
        elif choice == "3":
            show_supported_currencies()

        # ── Option 4: Exit ────────────────────────────────────
        elif choice == "4":
            print(f"\n👋 Goodbye, {user_name}! Happy converting. 💱\n")
            break

        else:
            print("❌ Invalid choice. Enter 1, 2, 3, or 4.")


# ─────────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()