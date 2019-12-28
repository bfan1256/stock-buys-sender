import csv
from algo_yf import buy_signal
import timeit
from email_sender import send_email
from tqdm import tqdm


start = timeit.default_timer()
def read_exchange(file):
    with open(file) as f:
        reader = csv.reader(f)
        symbols = []
        for line in reader: 
            symbols.append(line[0])
        f.close()
    return list(sorted(symbols[1:]))

exchanges = ['./exchanges/nasdaq.csv', './exchanges/nyse.csv']
all_symbols = []
print('Reading Exchange Data')
for exchange in exchanges:
    symbols = read_exchange(exchange)
    all_symbols += symbols
all_symbols = list(sorted(all_symbols))
print('Using {0} Symbols'.format(len(all_symbols)))

buys = []

for symbol in tqdm(all_symbols):
    try:
        if (buy_signal(symbol, under_value=20)):
            buys.append(symbol)
    except Exception: 
        continue

stop = timeit.default_timer()
print(buys)
print('Total Time: ', stop-start)
print('Sending Email to brandonfan1256@gmail.com...')
send_email('brandonfan1256@gmail.com', 'Brandon', buys)