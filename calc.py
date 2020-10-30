import csv
import datetime
from wallstreet import Stock, Call, Put


def closest_strike(price, strikes, option):
    aux = []
    for strike in strikes:
        aux.append(abs(price - strike))
    closest = aux.index(min(aux))
    first = strikes[closest]
    range = strikes[closest]-strikes[closest-1]
    allowed_range = range*.3
    option.set_strike(first)
    # this is modified to use .3 of the range between strikes. for instance, if the range between strikes for
    #  amazon is $10, the allowed range would be $3. If the closest strike of amazon is $100, and the price is $105 this
    #  math would look like:if (100-3=97) <= 100 <= (100+3=103), use this and return the option ask + option bid / 2
    if (price - allowed_range) <= strikes[closest] <= (price + allowed_range):
        return round(((option.ask + option.bid) / 2), 2)
    else:
        second = strikes[closest - 1]
        if price > strikes[closest]:
            second = strikes[closest + 1]
        average1 = (option.ask + option.bid) / 2
        option.set_strike(second)
        average2 = (option.ask + option.bid) / 2
        return round(((average1 + average2) / 2), 2)


def expected_move(price, call_price, put_price):
    em = call_price + put_price
    upper_em = price + em
    lower_em = price - em
    return round(em, 2), round(upper_em, 2), round(lower_em, 2)


"""so take last friday, pull closing price. 
Take the next weeks at the money call and at the money put (the same price it's at right now, as close as possible
closing price is actual 4:00pm.  options prices would be 4:00pm. for option use the mid if they have it, or the average
of bid and ask if they don't.  EMAIL THIS TO IPAU1@ICLOUD.COM"""


def stock_em_pm_data(stock_symbol):
    error = None
    stock = Stock(stock_symbol)
    stock_price = stock.price
    start_date = stock.last_trade
    print("The start date is %s" % start_date)
    time1 = datetime.datetime.strptime(start_date, "%d %b %Y %H:%M:%S")
    end_date = time1 + datetime.timedelta(days=7)
    # TODO FIX DATE PRINTOUT SO IT MATCHES START DATE FORMAT
    print("The end date is %s" % end_date)
    print('The stock %s was trading at %s' % (stock.name, stock_price))
    try:
        call = Call(stock_symbol, d=end_date.day, m=end_date.month, y=end_date.year)
        call_strikes = call.strikes
        closest_call_strike = closest_strike(stock_price, call_strikes, option=call)
        print('The ATM call is %s' % closest_call_strike)

        put = Put(stock_symbol, d=end_date.day, m=end_date.month, y=end_date.year)
        put_strikes = put.strikes
        closest_put_strike = closest_strike(stock_price, put_strikes, option=put)
        print('The ATM put is %s' % closest_put_strike)

        expected, upper_expected_move, lower_expected_move = expected_move(stock_price, closest_call_strike,
                                                                           closest_put_strike)
        print('The expected move is %s' % expected)
        print('The upper expected move is %s' % upper_expected_move)
        print('The lower expected move is %s' % lower_expected_move)
        potential_move = round((expected + closest_strike(upper_expected_move, call_strikes, option=call) +
                                closest_strike(lower_expected_move, put_strikes, option=put)), 2)
        print('The Potential Move is %s' % potential_move)
        upper_potential_move = stock_price + potential_move
        lower_potential_move = stock_price - potential_move
        upper_potential_move = round(upper_potential_move, 2)
        lower_potential_move = round(lower_potential_move, 2)
        print('The upper possible move is %s' % upper_potential_move)
        print('The lower possible move is %s' % lower_potential_move)
    except IndexError or LookupError:
        error = 'No Options'
        print("There's no options for that stock.")

    return {'stock symbol': stock_symbol, 'stock price': stock_price, 'start date': start_date, 'end date': end_date,
            'closest call strike': closest_call_strike, 'closest put strike': closest_put_strike,
            'expected move': expected, 'upper expected move': upper_expected_move,
            'lower expected move': lower_expected_move, 'potential move': potential_move,
            'upper potential move': upper_potential_move, 'lower potential move': lower_potential_move, 'error': error}


# ADD STOCKS TO THIS LIST. MAKE SURE THEY ARE IN THE NYSE. NINTENDO, FOR INSTANCE, WILL FAIL FOR OPTIONS CALLS
# IF YOU DON'T THINK IT HAS OPTIONS, DON'T PUT IT HERE.
stock_list = ['AAPL', 'BA', 'BRK-B', 'DIS', 'GE', 'HD', 'NKE', 'SBUX', 'VZ', 'MAR', 'VOO', 'EXPE', 'WORK', 'TSLA',
              'FUV', 'CAR', 'XYL', 'UBER', 'GOOG', 'HLT', 'FB', 'NKLA', 'BETZ', 'SPCE', 'CARR',
              'QQQ', 'NTAP', 'NFLX', 'AMD', 'NVDA', 'CRSP']

with open('stock_em_pm_calculated.csv', mode='w') as csv_file:
    fieldnames = ['stock symbol', 'stock price', 'start date', 'end date', 'closest call strike', 'closest put strike',
                  'expected move', 'upper expected move', 'lower expected move', 'potential move',
                  'upper potential move', 'lower potential move', 'error']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for stock in stock_list:
        em_pm_data = stock_em_pm_data(stock)
        writer.writerow(em_pm_data)
