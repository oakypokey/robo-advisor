#Setup
from dotenv import load_dotenv
import requests
import csv
import os
import datetime
from tabulate import tabulate  #Library that creates tables from arrays
import json
from urllib.parse import urlencode

#Get API key
load_dotenv()
API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")

#Init variables
user_symbols = ""
failure = False
results = {}

class StockData:
    def __init__(self, data):
        self.data = data
        self.latest_day = ""
        self.last_refreshed = ""
        self.latest_close = 0.00
        self.recent_high = 0.00
        self.recent_low = 0.00
        self.recommendation = ""
        self.reason = ""
        self.average_price = 0.00

        self.process_data(data)
    
    def process_data(self, data):
        firstTick = 0  #using this to capture only the first result
        sumPrice = 0

        if ("Error Message" in data):
            raise Exception(data["Error Message"])

        self.last_refreshed = data["Meta Data"]["3. Last Refreshed"]
        for time in data[
            "Time Series (Daily)"]:  #add all the info
            time_series_values = list(
            data["Time Series (Daily)"][time].values())

            if (firstTick == 0):
                date_values = time.split("-")
                self.latest_day = datetime.date(year=int(date_values[0]),
                                        month=int(date_values[1]),
                                        day=int(date_values[2]))
                self.latest_close = float(time_series_values[3])
                self.recent_low = float(time_series_values[2])
                self.firstTick = firstTick + 1

                if (self.recent_high < float(time_series_values[1])):
                    self.recent_high = float(time_series_values[1])

                if (self.recent_low > float(time_series_values[2])):
                    self.recent_low = float(time_series_values[2])
                    
                #summing all of the closing prices together for the average later on
                sumPrice = sumPrice + float(time_series_values[3])

        #sum of all prices divided by the number of points to get average over the period
        self.average_price = sumPrice / len(data["Time Series (Daily)"])

        [self.recommendation, self.reason] = self.recommendationEngine(self.average_price, self.latest_close)
    
    def get_stats(self):
        return {
            "latest_close": self.latest_close,
            "recent_high": self.recent_high,
            "recent_low": self.recent_low,
            "average_price": self.average_price
    
        }
    
    def get_recommendations(self):
        return {
            "recommendation": self.recommendation,
            "reason": self.reason
        }
    
    def get_data_stats(self):
        return {
            "latest_day": self.latest_day,
            "last_refreshed": self.last_refreshed
        }

    def recommendationEngine(self, averagePrice, latestClose):
        #if latestClose is above average, sell
        if(latestClose > averagePrice):
            return ["SELL", "Latest closing price was above the average."]
        else:
            return ["BUY", "Latest closing price was below the average."]
    
    def output_file(self):
        path = os.path.join(os.path.dirname(__file__),"..", "data", ticker + "_data.csv")
        csvFile = open(path,'w')  #open up csv to write to
        writer = csv.writer(csvFile)  #create csv writer
        writer.writerow(["time", "open", "high", "low", "close","volume"])  #insert header row

        for time in self.data["Time Series (Daily)"]:  #add all the info
            time_series_values = list(self.data["Time Series (Daily)"][time].values())
            writer.writerow([time] + time_series_values)
        
        csvFile.close()




#to_usd function for output
def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}"  #> $12,000.71

def compile_url(ticker):
    payload = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': ticker,
        'datatype': 'json',
        'apikey': API_KEY
        }
    return "https://www.alphavantage.co/query?" + urlencode(payload)

#checks if a string has ANY numbers in it
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


#Wrapper function for strip so I can use map()
def stripString(inputString):
    return inputString.strip()

def hasSpecial(inputString):
    return not inputString.isalnum()

def get_response(url):
   return requests.get(url).json()

if __name__ == "__main__":   
    #Ask user to submit choice, conver to upper case
    user_symbols = input(
        "Please enter a ticker symbol, or a series of ticker symbols seperated by a comma, to retrieve data: "
    ).upper()

    #Split up symbols and remove trailing white space
    user_symbols = list(map(stripString, user_symbols.split(',')))
    #Perfom error checking on each submission
    for symbol in user_symbols:
        #Check that ticker is less than 5 characters
        if (len(symbol) > 4):
            print("[ERROR]: Symbol '" + str(symbol) +
                "' has too many characters. Please try again.")
            failure = True
        #Check that ticker contains only contains letters
        if (hasNumbers(symbol)):
            print("[ERROR]: Symbol '" + str(symbol) +
                "' contains numbers. Please try again.")
            failure = True
        #Check that the ticker contains special characters
        if(hasSpecial(symbol)):
            print("[ERROR]: Symbol '" + str(symbol) +
                "' contains a special character. Please try again.")
            failure = True

    #If there are errors in the first wave, make requests for information

    if (not failure):
        #Begin output
        print("-------------------------")
        print("SELECTED SYMBOLS: ", ", ".join(user_symbols))
        print("-------------------------")
        print("REQUESTING STOCK MARKET DATA...")
        print("REQUEST AT: ", datetime.datetime.now().strftime("%D %I:%M%p"))
        print("-------------------------")

        #Making requests
        for ticker in user_symbols:

            try:

                request_result = get_response(compile_url(ticker))

                results[ticker] = StockData(request_result)  #adding request info to an array

                results[ticker].output_file()

                print("[SUCCESS] " + ticker + " data file has been created")

            except:
                print(
                    "[ERROR]: An error with the request occured. Skipping ticker "
                    + ticker + " | Response:  " + request_result["Error Message"])

        tickers = results.keys()

        tableData = {
            "ticker": [],
            "last_refreshed": [],
            "latest_day": [],
            "latest_close": [],
            "recent_high": [],
            "recent_low": []
        }

        recommendationData = {
            "ticker": [],
            "recommendation": [],
            "reason": [],
            "average_price": []
        }

        for symbol in tickers:
            summary_data = {**results[symbol].get_data_stats(), **results[symbol].get_stats(), **results[symbol].get_recommendations(), "ticker": symbol}

            for key in tableData.keys():
                tableData[key].append(summary_data[key])
            
            for key in recommendationData.keys():
                recommendationData[key].append(summary_data[key])

        print(
            " \n \n",
            tabulate(tableData,
                    headers=[
                        "Ticker", "Last Refreshed", "Latest Day", "Latest Close",
                        "Recent High", "Recent Low"
                    ],
                    tablefmt="grid"))
        
        print(
            " \n \n",
            tabulate(recommendationData,
                    headers=[
                        "Ticker", "Recommendation", "Reason", "Average Price"
                    ],
                    tablefmt="grid"))

        print("End of trading recommendations report. Good bye!")