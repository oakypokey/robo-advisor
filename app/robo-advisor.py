#Initial code

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY: 2018-02-20")
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

#to_usd function for output
def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

#checks if a string has ANY numbers in it
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

#Wrapper function for strip so I can use map()
def stripString(inputString):
    return inputString.strip()

#Setup
from dotenv import load_dotenv
import requests
import csv
import os
import datetime

#Get API key
load_dotenv()
API_KEY=os.environ.get("ALPHAVANTAGE_API_KEY")

#Init variables
user_symbols = ""
failure = False

#Ask user to submit choice, conver to upper case
user_symbols = input("Please enter a ticker symbol, or a series of ticker symbols seperated by a comma, to retrieve data: ").upper()

#Split up symbols and remove trailing white space
user_symbols = list(map(stripString, user_symbols.split(',')))
#Perfom error checking on each submission
for symbol in user_symbols:
    #Check that ticker is less than 5 characters
    if(len(symbol) > 4):
        print("[ERROR]: Symbol '"+str(symbol)+"' has too many characters. Please try again.")
        failure = True
    #Check that ticker contains only contains letters
    if(hasNumbers(symbol)):
        print("[ERROR]: Symbol '"+str(symbol)+"' contains numbers. Please try again.")
        failure = True

print(user_symbols)