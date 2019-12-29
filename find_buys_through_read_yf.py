import csv
import uuid
import algo_yf as algo
import timeit
import pickle
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
print('Reading Stock Data')
with open('yahoo-data.p', 'rb') as f:
    data = pickle.load(f)
    f.close()
for symbol in tqdm(all_symbols):
    try:
        if (algo.buy_signal(data[symbol], under_value=10)):
            buys.append(symbol)
    except Exception as e:
        continue

if len(buys) > 0:
    print('Getting Fundamental Data for Buy Signal Stocks...')
    rows = [['Symbol', 'Business Summary', 'Sector', 'Forward EPS', 'Forward P/E', 'P/B']]
    for buy in tqdm(buys):
        buy_info = algo.get_stock_info(buy)
        row = [buy] + buy_info
        rows.append(row)
    new_id = uuid.uuid1()
    file_name = './runs/{0}.csv'.format(new_id)
    with open(file_name, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
        f.close()
    print('Sending Email to brandonfan1256@gmail.com...')
    send_email('brandonfan1256@gmail.com', 'Brandon', buys, file_name)
else:
    print('No buys were found today...')