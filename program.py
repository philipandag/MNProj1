#US dollar and one troy ounce of silver
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from functions import *
import math
from datetime import datetime
from datetime import timedelta

# Odczytanie danych
data = read_data()
data = data.to_numpy()


def __datetime(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()


# Przygotowanie danych
values = data[:, 1]
times = data[:, 0]
for t in range(len(times)):
    times[t] = __datetime(times[t].split(" ")[0])

def EMAn(data, start_index, N):
    end_index = start_index - N
    if(end_index < 0):
        end_index = 0
    if(start_index == end_index):
        return 0       
    
    a = 2/(N+1)
    nominator = 0
    denominator = 0
    common = 1 # (1-a)^i
    for i in range(start_index, end_index, -1):
        nominator += data[i]*common
        denominator += common
        common *= (1-a)
    return nominator/denominator

def macd(data, index):
    return EMAn(data, index, 12) - EMAn(data, index, 26)


#Obliczenie wartości MACD i SIGNAL
MACD = np.array([])
for i in range(0, len(values)):
    MACD = np.append(MACD, macd(values, i))
SIGNAL = np.array([])
for i in range(0, len(values)):
    SIGNAL = np.append(SIGNAL, EMAn(MACD, i, 9))


# Odczytanie sygnałów kupna i sprzedaży
sells_on_MACD = [[], []]
sells_on_price = [[], []]
buys_on_MACD = [[], []]
buys_on_price = [[], []]
for i in range(0, len(values)):
    if(MACD[i]-SIGNAL[i] < 0 and MACD[i-1]-SIGNAL[i-1] > 0):
        sells_on_MACD[0].append(times[i])
        sells_on_MACD[1].append(MACD[i])
        sells_on_price[0].append(times[i])
        sells_on_price[1].append(values[i])
    elif(MACD[i]-SIGNAL[i] > 0 and MACD[i-1]-SIGNAL[i-1] < 0):
        buys_on_MACD[0].append(times[i])
        buys_on_MACD[1].append(MACD[i])
        buys_on_price[0].append(times[i])
        buys_on_price[1].append(values[i])


# Wykres kursu
plt.plot(times, values, linewidth=0.5)
plt.title('Kurs srebra w USD')
plt.legend(["Kurs XAG"])
plt.xlabel("Data")
plt.ylabel("USD")
plt.show()

# Formatowanie daty
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=60))
plt.gcf().autofmt_xdate()


# Wykres kursu z sygnałami kupna i sprzedaży
plt.plot(times, values, linewidth=0.5)
plt.title('Kurs srebra w USD')
plt.xlabel("Data")
plt.ylabel("USD")

# Formatowanie daty
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=10))
plt.gcf().autofmt_xdate()

# Naniesienie sygnałów na wykres kursu
plt.plot(sells_on_price[0], sells_on_price[1], 'rx')
plt.plot(buys_on_price[0], buys_on_price[1], 'gx')

# Utworzenie strzałek symbolizujących pary kupno-sprzedaż
i = 0
j = 0
end = min(len(sells_on_price[0]), len(buys_on_price[0]))
profitable_trades = []
unprofitable_trades = []
while i < end and j < end:
    # Jeżeli sprzedaż nastąpiła przed kupnem, to przesuń indeks sprzedaży aby strzałka zaczynała się od kupna
    if sells_on_price[0][i] < buys_on_price[0][j]:
        i+=1

    arrow = ((buys_on_price[0][j]), # x
             (buys_on_price[1][j]), # y
              (sells_on_price[0][i] - buys_on_price[0][j]).days, # dx 
              (sells_on_price[1][i] - buys_on_price[1][j]) # dy
            )
    
    if buys_on_price[1][j] < sells_on_price[1][i]:
        profitable_trades.append(arrow)
    else:   
        unprofitable_trades.append(arrow)

    j += 1
    i += 1

# Niewidoczne linie służące do oznaczenia strzałek w legendzie
plt.plot([times[0]],[values[0]], '-g')
plt.plot([times[0]],[values[0]], '-r')

# Rysowanie strzałek
for i in range(len(profitable_trades)):
    plt.arrow(x = profitable_trades[i][0], y = profitable_trades[i][1], 
            dx = profitable_trades[i][2], dy = profitable_trades[i][3],
            edgecolor='green', linewidth=0.5)
    
for i in range(len(unprofitable_trades)):
    plt.arrow(x = unprofitable_trades[i][0], y = unprofitable_trades[i][1], 
            dx = unprofitable_trades[i][2], dy = unprofitable_trades[i][3],
            edgecolor='red', linewidth=0.5)
plt.legend(["Kurs XAG", "Sygnał sprzedaży", "Sygnał kupna", "Zyski", "Straty"])
plt.show()




# Wykres MACD i SIGNAL
plt.plot(times, MACD, linewidth=0.5)
plt.plot(times, SIGNAL, linewidth=0.5)

# Naniesienie sygnałów na wykres MACD i SIGNAL
sell = plt.plot(sells_on_MACD[0], sells_on_MACD[1], 'rx')
buy = plt.plot(buys_on_MACD[0], buys_on_MACD[1], 'gx')
plt.legend(["MACD", "SIGNAL", "Sygnał sprzedaży", "Sygnał kupna"])
plt.title('Linie MACD i SIGNAL')
plt.xlabel("Data")
plt.axhline(y = 0, color='black', linewidth=0.5)

# Formatowanie daty
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=60))
plt.gcf().autofmt_xdate()
plt.show()



# Symulacja
class Client:
    def __init__(self, starting_money):
        self.dollars = starting_money
        self.silver = 0
    def buy_all(self, price):
        amount = math.floor(self.dollars/price)
        self.silver += amount
        self.dollars -= round(amount*price, 2)
    def sell_all(self, price):
        self.dollars += round(self.silver*price, 2)
        self.silver = 0


client = Client(starting_money=1000)
money = []
silver = []
print(client.dollars)
for i in range(0, len(values)):
    money.append(client.dollars)
    silver.append(client.silver)

    if (MACD[i]-SIGNAL[i] < 0 and MACD[i-1]-SIGNAL[i-1] > 0):       
        client.sell_all(values[i])
    elif MACD[i]-SIGNAL[i] > 0 and MACD[i-1]-SIGNAL[i-1] < 0:
        client.buy_all(values[i])

client.sell_all(values[len(values)-1])
print(client.dollars)





