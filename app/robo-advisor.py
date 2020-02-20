#Setup
from dotenv import load_dotenv
import requests
import csv
import os
import datetime
from tabulate import tabulate #Library that creates tables from arrays
import json

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


#checks if a string has ANY numbers in it
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


#Wrapper function for strip so I can use map()
def stripString(inputString):
    return inputString.strip()

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
        payload = {'function': 'TIME_SERIES_DAILY', 'symbol': ticker, 'datatype': 'json', 'apikey': API_KEY}
        
        request_result = requests.get("https://www.alphavantage.co/query", params=payload).json()
        
        if(request_result["Error Message"]):
            print("[ERROR]: An error with the request occured. Skipping ticker " + ticker + " | " + request_result["Error Message"])
            break

        results[ticker] = request_result #adding request info to an array


        csvFile = open("./data/" + ticker + "_data.csv", 'w') #open up csv to write to
        writer = csv.writer(csvFile) #create csv writer
        writer.writerow(["time", "open", "high", "low", "close", "volume"]) #insert header row
        
        for time in request_result["Time Series (Daily)"]: #add all the info
            writer.writerow([time] + list(request_result["Time Series (Daily)"][time].values()))

else:
    print("Please try again")
