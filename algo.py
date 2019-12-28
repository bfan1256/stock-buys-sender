from alpha_vantage.techindicators import TechIndicators

def buy_signal(symbol): 
    indicators = TechIndicators(key='2OY123W8XM7CG388', output_format='pandas')
    ema_50 = indicators.get_ema(symbol, time_period=50)[0].iloc[-1]['EMA']
    print(ema_50)
    ema_100 = indicators.get_ema(symbol, time_period=100)[0].iloc[-1]['EMA']
    ema_150 = indicators.get_ema(symbol, time_period=150)[0].iloc[-1]['EMA']
    over_100 = ema_50 > ema_100
    under_150 = ema_100 < ema_150
    return over_100 and under_150


def sell_signal(symbol): 
    ema_20 = indicators.get_ema(symbol, time_period=50)
    ema_100 = indicators.get_ema(symbol, time_period=100)
    ema_150 = indicators.get_ema(symbol, time_period=150)
    return ema(close, 20) < ema(close, 150) and ema(close, 100) < ema(close, 150)