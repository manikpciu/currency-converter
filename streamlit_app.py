# -*- coding: utf-8 -*-
# ============================================================
#  Currency Converter — Streamlit Web App
#  Module 4 Project | Python OOP
# ============================================================

import streamlit as st
from datetime import datetime

# ─────────────────────────────────────────────
#  Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Currency Converter",
    page_icon="💱",
    layout="centered"
)

# ─────────────────────────────────────────────
#  Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #0f0f1a 100%);
    min-height: 100vh;
}

.main-title {
    text-align: center;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(90deg, #00d4ff, #7b2ff7, #00d4ff);
    background-size: 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s infinite linear;
    margin-bottom: 0.2rem;
}

@keyframes shimmer {
    0% { background-position: 0% }
    100% { background-position: 200% }
}

.subtitle {
    text-align: center;
    color: #888;
    font-size: 0.95rem;
    margin-bottom: 2rem;
    font-family: 'DM Mono', monospace;
}

.result-card {
    background: linear-gradient(135deg, #1e1e3a, #2a1a4e);
    border: 1px solid #7b2ff7;
    border-radius: 16px;
    padding: 1.8rem;
    text-align: center;
    margin: 1.5rem 0;
    box-shadow: 0 0 30px rgba(123, 47, 247, 0.3);
}

.result-amount {
    font-size: 2.4rem;
    font-weight: 800;
    color: #00d4ff;
    font-family: 'DM Mono', monospace;
}

.result-label {
    color: #aaa;
    font-size: 0.9rem;
    margin-top: 0.4rem;
}

.log-entry {
    background: #111128;
    border-left: 3px solid #7b2ff7;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    margin: 0.4rem 0;
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    color: #ccc;
}

.rate-badge {
    display: inline-block;
    background: #1a1a2e;
    border: 1px solid #333;
    border-radius: 8px;
    padding: 0.3rem 0.7rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    color: #00d4ff;
    margin: 0.2rem;
}

.section-header {
    color: #7b2ff7;
    font-size: 1rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin: 1.5rem 0 0.8rem 0;
}

div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stTextInput"] label {
    color: #aaa !important;
    font-size: 0.85rem;
    font-family: 'DM Mono', monospace;
}

div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #7b2ff7, #00d4ff);
    color: white;
    border: none;
    border-radius: 10px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    padding: 0.6rem 2rem;
    width: 100%;
    font-size: 1rem;
    transition: opacity 0.2s;
}

div[data-testid="stButton"] button:hover {
    opacity: 0.85;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Logger Class  (Association)
# ─────────────────────────────────────────────
class Logger:
    def log(self, user: str, amount: float, result: str) -> dict:
        return {
            "time": datetime.now().strftime("%H:%M:%S"),
            "user": user,
            "amount": amount,
            "result": result
        }


# ─────────────────────────────────────────────
#  CurrencyConverter Class
# ─────────────────────────────────────────────
class CurrencyConverter:
    exchange_rates = {
        "USD": 1.0,
        "BDT": 110.50,
        "EUR": 0.92,
        "GBP": 0.79,
        "JPY": 149.50,
        "INR": 83.12,
        "CAD": 1.36,
        "AUD": 1.53,
        "SAR": 3.75,
        "AED": 3.67,
    }

    def __init__(self, amount: float, from_currency: str, to_currency: str):
        self.amount        = amount
        self.from_currency = from_currency.upper()
        self.to_currency   = to_currency.upper()

    def convert(self) -> float | None:
        if not CurrencyConverter.is_valid_code(self.from_currency):
            return None
        if not CurrencyConverter.is_valid_code(self.to_currency):
            return None
        amount_in_usd = self.amount / CurrencyConverter.exchange_rates[self.from_currency]
        converted     = amount_in_usd * CurrencyConverter.exchange_rates[self.to_currency]
        return round(converted, 4)

    @classmethod
    def update_rate(cls, currency_code: str, new_rate: float) -> bool:
        code = currency_code.upper()
        if cls.is_valid_code(code):
            cls.exchange_rates[code] = new_rate
            return True
        return False

    @staticmethod
    def is_valid_code(code: str) -> bool:
        return code.upper() in CurrencyConverter.exchange_rates


# ─────────────────────────────────────────────
#  Session State Init
# ─────────────────────────────────────────────
if "logs" not in st.session_state:
    st.session_state.logs = []

# ─────────────────────────────────────────────
#  UI
# ─────────────────────────────────────────────
st.markdown('<div class="main-title">💱 Currency Converter</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Module 4 Project · Python OOP · Real-time Conversion</div>', unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔄 Convert", "⚙️ Update Rate", "📋 Logs"])

# ════════════════════════════════════════════
#  TAB 1 — Convert
# ════════════════════════════════════════════
with tab1:
    user_name = st.text_input("Your Name", placeholder="Enter your name...")

    currencies = list(CurrencyConverter.exchange_rates.keys())
    currency_labels = {
        "USD": "🇺🇸 USD — US Dollar",
        "BDT": "🇧🇩 BDT — Bangladeshi Taka",
        "EUR": "🇪🇺 EUR — Euro",
        "GBP": "🇬🇧 GBP — British Pound",
        "JPY": "🇯🇵 JPY — Japanese Yen",
        "INR": "🇮🇳 INR — Indian Rupee",
        "CAD": "🇨🇦 CAD — Canadian Dollar",
        "AUD": "🇦🇺 AUD — Australian Dollar",
        "SAR": "🇸🇦 SAR — Saudi Riyal",
        "AED": "🇦🇪 AED — UAE Dirham",
    }

    col1, col2 = st.columns(2)
    with col1:
        from_cur = st.selectbox("From", currencies,
                                format_func=lambda x: currency_labels[x],
                                index=currencies.index("BDT"))
    with col2:
        to_cur = st.selectbox("To", currencies,
                              format_func=lambda x: currency_labels[x],
                              index=currencies.index("USD"))

    amount = st.number_input("Amount", min_value=0.0, value=100.0, step=1.0)

    if st.button("Convert Now"):
        if amount <= 0:
            st.error("Amount must be greater than 0.")
        else:
            converter = CurrencyConverter(amount, from_cur, to_cur)
            result    = converter.convert()

            if result is not None:
                result_str = f"{amount} {from_cur} = {result} {to_cur}"
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-label">{amount:,} {from_cur}</div>
                    <div style="color:#7b2ff7;font-size:1.5rem;margin:0.3rem 0;">▼</div>
                    <div class="result-amount">{result:,} {to_cur}</div>
                    <div class="result-label" style="margin-top:0.8rem;">
                        1 {from_cur} = {round(CurrencyConverter.exchange_rates[to_cur]/CurrencyConverter.exchange_rates[from_cur], 4)} {to_cur}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Logger — Association (passed from outside)
                logger     = Logger()
                log_entry  = logger.log(user_name or "Anonymous", amount, result_str)
                st.session_state.logs.append(log_entry)
            else:
                st.error("Invalid currency code!")

    # ── Exchange Rates Display ─────────────────
    st.markdown('<div class="section-header">Live Rates (vs USD)</div>', unsafe_allow_html=True)
    badges = ""
    for code, rate in CurrencyConverter.exchange_rates.items():
        badges += f'<span class="rate-badge">1 USD = {rate} {code}</span>'
    st.markdown(badges, unsafe_allow_html=True)


# ════════════════════════════════════════════
#  TAB 2 — Update Rate
# ════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">Update Exchange Rate</div>', unsafe_allow_html=True)
    st.caption("Update mock exchange rates (vs USD base)")

    currencies = list(CurrencyConverter.exchange_rates.keys())
    update_cur  = st.selectbox("Select Currency", currencies,
                               format_func=lambda x: currency_labels[x],
                               key="update_cur")
    current_val = CurrencyConverter.exchange_rates[update_cur]
    new_rate    = st.number_input(f"New Rate for {update_cur} (current: {current_val})",
                                  min_value=0.0001, value=float(current_val), step=0.01)

    if st.button("Update Rate"):
        success = CurrencyConverter.update_rate(update_cur, new_rate)
        if success:
            st.success(f"✅ Updated: 1 USD = {new_rate} {update_cur}")
        else:
            st.error("Invalid currency code!")


# ════════════════════════════════════════════
#  TAB 3 — Logs
# ════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Conversion History</div>', unsafe_allow_html=True)

    if not st.session_state.logs:
        st.info("No conversions yet. Go to Convert tab to get started!")
    else:
        for entry in reversed(st.session_state.logs):
            st.markdown(f"""
            <div class="log-entry">
                🕐 {entry['time']} &nbsp;|&nbsp;
                👤 {entry['user']} &nbsp;|&nbsp;
                💰 {entry['result']}
            </div>
            """, unsafe_allow_html=True)

        if st.button("Clear Logs"):
            st.session_state.logs = []
            st.rerun()
