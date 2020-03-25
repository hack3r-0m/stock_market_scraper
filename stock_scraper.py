from bs4 import BeautifulSoup
from time import sleep
from requests import get,ConnectionError

class Main():

    def __init__(self):
        self.useragent = { 'useragent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7) AppleWebKit/534.24 (KHTML, like Gecko) Iron/11.0.700.2 Chrome/11.0.700.2 Safari/534.24'
                        }

    def build_connection(self):
    
        url = 'https://www.moneycontrol.com/stocks/marketstats/indexcomp.php?optex=NSE&opttopic=indexcomp&index=9'
        response = get(url, headers=self.useragent)

        if response.status_code != 200:
            raise ConnectionError("Expected status code 200, but got {}".format(response.status_code))

        print("connection established : {}".format(response.status_code))

        return response


    def build_scrapper(self, response):

        raw_soup = BeautifulSoup(response.text, 'lxml')
        trows = raw_soup.find_all('tr')

        all_items = []

        for trow in trows:
            td = trow.find_all('td')
            row = [x.text for x in td]
        
            if row != [] and row != ['']:
                all_items.append(row)

        # for removing last two unwanted items
        all_items.pop()
        all_items.pop()

        return all_items

    def seperating_parameters(self, all_items):

        stock_names = []
        last_prices = []
        changes = []
        percent_changes = []

        for i in range(len(all_items)):

            stock_names.append(all_items[i][0].split("\n\n\n\n\n")[0])
            last_prices.append(all_items[i][2].replace(",",''))
            changes.append(all_items[i][3])
            percent_changes.append(all_items[i][4])

        return stock_names, last_prices, changes, percent_changes

    def notifier(self, previous_price, latest_price, stock_names):

        for i in range(len(stock_names)):

            for x in range(len(previous_price)):
            
                # converting to float for calculations
                
                previous_price[x] = float(previous_price[x])
                latest_price[x] = float(previous_price[x])


            offset = 0.02*(latest_price[i]-previous_price[i])

            '''
            if latest_price is less than previous_price then offset is positive
            '''
            print('checking {}'.format(stock_names[i]))

            if latest_price[i] < previous_price[i] - offset:
                print("Alert for {}".format(stock_names[i]))

                with open("alert.txt", 'a+') as board:
                    board.writelines("Alert for {}".format(stock_names[i]))

def recursifier():

    pointer = Main()
    pointer_connection = pointer.build_connection()
    stocks_primary_data = pointer.build_scrapper(pointer_connection)
    _names, pointer_prices, pointer_changes, pointer_percent_chg  = pointer.seperating_parameters(stocks_primary_data)

    pointer.notifier(intial_prices, pointer_prices, _names)
    print("waiting 30 seconds")
    sleep(30)
    print("Updated")

    recursifier()


initial = Main()

first_connection = initial.build_connection()
initial_stocks_primary_data = initial.build_scrapper(first_connection)
_names, intial_prices, initial_changes, initial_percent_chg  = initial.seperating_parameters(initial_stocks_primary_data)

print("Process Started!, waiting 30 seconds")
sleep(30)
print("waiting")
recursifier()
