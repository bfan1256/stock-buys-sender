import yfinance as yf

def buy_signal(symbol, under_value=None): 
    closing_data = compute_emas_buy(symbol, under_value=under_value)
    if closing_data is not False:
        today = closing_data.iloc[-1]
        over_50 = today['Close'] > today['EMA_50']
        over_100 = today['EMA_50'] > today['EMA_100']
        under_150 = today['EMA_100'] < today['EMA_150']
        signal = over_50 and over_100 and under_150
        return signal
    else:
        return False

def download_yf_data(symbols, multithread=True):
    symbol_string = ' '.join(symbols)
    data = yf.download(symbol_string, period='1y', actions=False, group_by='ticker', threads=multithread)
    return data

def compute_emas_buy(stock, under_value=None): 
    if under_value is not None:
        if stock['Close'].iloc[-1] > under_value:
            return False
    closing_data = stock.copy()
    closing_data['EMA_50'] = _calculate_ema(closing_data)['Close']
    closing_data['EMA_100'] = _calculate_ema(closing_data, span=100)['Close']
    closing_data['EMA_150'] = _calculate_ema(closing_data, span=150)['Close']
    closing_data = closing_data[['Close', 'EMA_50', 'EMA_100', 'EMA_150']]
    return closing_data

def compute_emas_sell(symbol): 
    stock_data = yf.Ticker(symbol)
    closing_data = stock_data.history(period='1y', actions=False)
    closing_data['EMA_20'] = _calculate_ema(closing_data, span=20)['Close']
    closing_data['EMA_100'] = _calculate_ema(closing_data, span=100)['Close']
    closing_data['EMA_150'] = _calculate_ema(closing_data, span=150)['Close']
    closing_data = closing_data[['Close', 'EMA_20', 'EMA_100', 'EMA_150']]
    return closing_data


def _calculate_ema(stock_data, span=50):
    ewm = stock_data.ewm(span=span, min_periods=0, adjust=False, ignore_na=False).mean()
    return ewm

def get_stock_info(symbol):
    stock_data = yf.Ticker(symbol)
    try:
        info = stock_data.info
    except Exception:
        return ['', '', None, None, None]
    return [info['longBusinessSummary'], info['sector'], info['forwardEps'], info['forwardPE'], info['priceToBook']]


def sell_signal(symbol): 
    closing_data = compute_emas_sell(symbol)
    today = closing_data.tail(1)
    return today['EMA_20'] < today['EMA_150'] and today['EMA_20'] < today['EMA_150']

if __name__ == "__main__":
    buy_signal('MSFT')