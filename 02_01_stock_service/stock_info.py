import yfinance as yf

# 예: 애플(AAPL) 티커
ticker = yf.Ticker("AAPL")
info = ticker.info

# 재무제표(Financials)
def financial_statements():
    return {
        'income_statement': ticker.financials,
        'balance_sheet': ticker.balance_sheet,
        'cash_flow': ticker.cashflow,
    }

def value_evaluation():
    return {
        'PER': info.get('trailingPE'),
        'PBR': info.get('priceToBook'),
        'PSR': info.get('priceToSalesTrailing12Months'),
        'dividend_yield': info.get('dividendYield'),
        'ROE': info.get('returnOnEquity'),
    }

def blue_chip_stock():
    return {
        'ROE': info.get('returnOnEquity'),
        'ROA': info.get('returnOnAssets'),
        'current_ratio': info.get('currentRatio'),
        'debt_to_equity': info.get('debtToEquity'),
        'profit_margin': info.get('profitMargins'),
    }

def volume():
    hist = ticker.history(period="1mo")
    return {
        'volume': hist['Volume'],
        'open': hist['Open'],
        'high': hist['High'],
        'low': hist['Low'],
        'close': hist['Close'],
    }    