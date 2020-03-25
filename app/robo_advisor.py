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

def compile_url(params):
    return "https://www.alphavantage.co/query?" + urlencode(params)

#checks if a string has ANY numbers in it
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


#Wrapper function for strip so I can use map()
def stripString(inputString):
    return inputString.strip()

def recommendationEngine(averagePrice, latestClose):
    #if latestClose is above average, sell
    if(latestClose > averagePrice):
        return ["SELL", "Latest closing price was above the average."]
    else:
        return ["BUY", "Latest closing price was below the average."]

def hasSpecial(inputString):
    return not inputString.isalnum()

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
            #creating the payload to send with the request
            payload = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': ticker,
                'datatype': 'json',
                'apikey': API_KEY
            }

            try:
                request_result = requests.get(compile_url(payload)).json()

                requests.get

                if ("Error Message" in request_result):
                    raise Exception(request_result["Error Message"])

                results[ticker] = request_result  #adding request info to an array

                path = os.path.join(os.path.dirname(__file__),"..", "data", ticker + "_data.csv")
                csvFile = open(path,
                            'w')  #open up csv to write to
                writer = csv.writer(csvFile)  #create csv writer
                writer.writerow(["time", "open", "high", "low", "close",
                                "volume"])  #insert header row

                #Init variables for ouptut statistics for the ticker
                latest_day = ""
                last_refreshed = request_result["Meta Data"]["3. Last Refreshed"]
                latest_close = 0.00
                recent_high = 0.00
                recent_low = 0.00
                recommendation = ""
                reason = ""
                averagePrice = 0.00
                sumPrice = 0.00

                firstTick = 0  #using this to capture only the first result

                for time in request_result[
                        "Time Series (Daily)"]:  #add all the info
                    time_series_values = list(
                        request_result["Time Series (Daily)"][time].values())

                    if (firstTick == 0):
                        date_values = time.split("-")
                        latest_day = datetime.date(year=int(date_values[0]),
                                                month=int(date_values[1]),
                                                day=int(date_values[2]))
                        latest_close = float(time_series_values[3])
                        recent_low = float(time_series_values[2])
                        firstTick = firstTick + 1

                    writer.writerow([time] + time_series_values)

                    if (recent_high < float(time_series_values[1])):
                        recent_high = float(time_series_values[1])

                    if (recent_low > float(time_series_values[2])):
                        recent_low = float(time_series_values[2])
                    
                    #summing all of the closing prices together for the average later on
                    sumPrice = sumPrice + float(time_series_values[3])

                #sum of all prices divided by the number of points to get average over the period
                averagePrice = sumPrice / len(request_result["Time Series (Daily)"])

                [recommendation, reason] = recommendationEngine(averagePrice, latest_close)

                #Output the data
                results[ticker]["Summary Data"] = {
                    "last_refreshed": last_refreshed,
                    "latest_day": latest_day,
                    "latest_close": to_usd(latest_close),
                    "recent_high": to_usd(recent_high),
                    "recent_low": to_usd(recent_low),
                    "ticker": ticker,
                    "recommendation": recommendation,
                    "reason": reason,
                    "averagePrice": to_usd(averagePrice)
                }

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
            "averagePrice": []
        }

        for symbol in tickers:
            for key in tableData.keys():
                tableData[key].append(results[symbol]["Summary Data"][key])
            
            for key in recommendationData.keys():
                recommendationData[key].append(results[symbol]["Summary Data"][key])

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