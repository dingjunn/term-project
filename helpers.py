import requests
import pprint
import yfinance

ticker = 'tsla' 
parameter = 'price'

url = f"https://yahoo-finance127.p.rapidapi.com/{parameter}/{ticker}"

headers = {
	"X-RapidAPI-Key": "c72f7a4367mshfe65ee4a74a894fp176ec0jsn93a89c3102d3",
	"X-RapidAPI-Host": "yahoo-finance127.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)

pprint.pprint(response.text)




import yfinance

def get_stock_info(ticker):
    """
    Fetch real-time stock data from Yahoo Finance, return current stock price based on the ticker input
    
    Parameters:
        ticker (str): The stock ticker symbol
        
    Returns:
        str: A formatted string with the stock information
    """
    # Get the stock data from Yahoo Finance
    stock_data = yfinance.Ticker(ticker).info
    
    # Extract the relevant information from the stock data
    stock_name = stock_data['longName']
    stock_price = stock_data['regularMarketPrice']
    stock_change = stock_data['regularMarketChange']
    stock_percent_change = stock_data['regularMarketChangePercent']
    
    # Format the string with the stock information
    stock_info = f"Stock Name: {stock_name}\nCurrent Price: {stock_price}\nChange: {stock_change} ({stock_percent_change}%)"
    
    return stock_info

info = get_stock_info('AAPL')
print(info)


def data_display(ticker):
    """
    Parse and display stock data and extract relevant information: the company description, growth graph to display to the user
    
    Parameters:
        ticker (str): The stock ticker symbol
        
    Returns:
        None
    """
    # Get relevant stock information
 

def add_portfolio():
    """
    This function could take a stock symbol and quantity as input and add the stock to the user's portfolio
    """
    if stock_symbol in portfolio:
        portfolio[stock_symbol] += quantity
    else:
        portfolio[stock_symbol] = quantity

def portfolio_growth():
    """
    This function will use historical stock price data of portofolio to caculate the projected growth rate.
    """
    pass

def portfolio_diversification():
    """
    This function will evaluate the diversification of portfolio across different sectors, industries, and asset classes
    """
    pass

def portfolio_risk():
    """
    This function will evaluate the risk of portfolio by caculating its variance and covariance 
    """
    pass

def data_store():
    """
    This function will help us store the record of portofolio with its return, risk and diversity created by the users to help users compare and do further analysis
    """

def main():
    # info = get_stock_info('AAPL')
    # print(info)


 if __name__ == "__main__":
    main()