from app.robo_advisor import StockData
from api_response_processing_test import test_response
import os
from os import listdir
from os.path import isfile, join
import csv

def test_output_file_creation():
    result = StockData(test_response)
    try:
        result.output_file()
    except:
        assert False
    
    fileName = test_response["Meta Data"]["2. Symbol"] + "_data.csv"
    filePath = os.path.join(os.path.dirname(__file__),"..", "data", fileName)
    dataPath = os.path.join(os.path.dirname(__file__),"..", "data")

    outputFiles = [output for output in listdir(dataPath) if isfile(join(dataPath, output))]

    assert fileName in outputFiles

    os.remove(filePath)

def test_output_file_contents():
    result = StockData(test_response)
    result.output_file()

    fileName = test_response["Meta Data"]["2. Symbol"] + "_data.csv"
    filePath = os.path.join(os.path.dirname(__file__),"..", "data", fileName)

    testRows = test_response["Time Series (Daily)"]

    with open(filePath, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            assert testRows[row["time"]]["1. open"] == row["open"]
            assert testRows[row["time"]]["2. high"] == row["high"]
            assert testRows[row["time"]]["3. low"] == row["low"]
            assert testRows[row["time"]]["4. close"] == row["close"]
            assert testRows[row["time"]]["5. volume"] == row["volume"]

    os.remove(filePath)