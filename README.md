# Robo-Advisor

This software allows users to interact with stock price information made available by Alphavantage through the command line.

## Installation
1. After cloning this repo, create a `.env` file within the main directory.
2. Obtain an API key from Alphavantage (https://www.alphavantage.co/)
3. Open the `.env` file using a text editor and paste the following

```
ALPHAVANTAGE_API_KEY="abc1234"
```

Then replace abc1234 with the API key you recieved from Alphavantage

4. Install the required dependencies using pip

```
pip install -r requirements.txt
```
5. To run the program, execute `app/robo-advisor.py`. For example, you could do it the following way:

```
python app/robo-advisor.py
```

6. Follow the instructions in the program itself.