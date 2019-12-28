import csv
from algo import buy_signal

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
print(all_symbols[:5])
print('Using {0} Symbols'.format(len(all_symbols)))

buys = []

for symbol in all_symbols:
    if (buy_signal(symbol)):
        buys.append(symbol)

print(buys)