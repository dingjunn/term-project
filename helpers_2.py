import yfinance as yf
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def get_stock_info(ticker):
    """
    Fetch historical stock data from Yahoo Finance based on the ticker input.
    
    Parameters:
        ticker (str): The stock ticker symbol
        
    Returns:
        dict: A dictionary containing relevant stock information
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    
    # Get historical market data for the past month
    hist = stock.history(period="1mo")
    
    # Get income statement and balance sheet data
    # income_stmt = stock.financials
    # balance_sheet = stock.balance_sheet
    
    currency = info['currency']
    exchange = info['exchange']
    name = info['shortName']
    
    # Format historical market data as a string
    hist_str = '\nHistorical Market Data (Past Month):\n' + hist.to_string()
    
    # Create dictionary with relevant stock information
    stock_info = {
        'name': name,
        'ticker': ticker,
        'currency': currency,
        'exchange': exchange,
        'hist': hist,
        'info': info
    }
    
    return stock_info

def data_display(ticker):
    """
    Parse and display stock data and extract relevant information: the company description, growth graph to display to the user
    
    Parameters:
        ticker (str): The stock ticker symbol
        
    Returns:
        dict: A dictionary containing company description and historical market data
    """
    # Get relevant stock information
    stock_info = get_stock_info(ticker)
    name = stock_info['name']
    ticker = stock_info['ticker']
    currency = stock_info['currency']
    exchange = stock_info['exchange']
    hist = stock_info['hist']
    info = stock_info['info']
    # Print out company description
    print(f"{name} ({ticker}) is traded on {exchange} in {currency}. {info['longBusinessSummary']}\n")
    
    # Plot historical market data
    plt.plot(hist['Close'])
    plt.title(f"{name} ({ticker}) Historical Close Price")
    plt.xlabel("Date")
    plt.ylabel(f"Close Price ({currency})")
    plt.show()
    
    # Create dictionary with company description and historical market data
    data_dict = {
        'company': {
            'name': name,
            'ticker': ticker,
            'currency': currency,
            'exchange': exchange,
            'description': info['longBusinessSummary']
        },
        'historical_data': hist
    }
    
    return data_dict

# Example usage of data_display function
# data = data_display('AAPL')
# print(data)
# data_display("AAPL")

def portfolio_growth(portfolio):
    """
    This function will use historical stock price data of a portfolio to calculate the projected growth rate.
    
    Parameters:
        portfolio (dict): A dictionary containing stocks in the portfolio and their quantities.
            Example: {'AAPL': 10, 'GOOG': 5, 'MSFT': 20}
    
    Returns:
        float: The projected growth rate of the portfolio based on historical stock data
    """
    total_value = 0
    total_cost = 0
    for stock, quantity in portfolio.items():
        # Get historical market data for the stock
        hist = yf.Ticker(stock).history(period="1mo")
        # Get the latest close price of the stock
        latest_price = hist['Close'].iloc[-1]
        # Calculate the total value and cost of the stock in the portfolio
        stock_value = latest_price * quantity
        stock_cost = hist['Close'].iloc[0] * quantity
        total_value += stock_value
        total_cost += stock_cost
    # Calculate the growth rate as the ratio of total value to total cost
    growth_rate = (total_value - total_cost) / total_cost
    return growth_rate


def portfolio_diversification(portfolio):
    """
    Display the industry information of the stocks in the portfolio to show diversification.
    
    Parameters:
        portfolio (dict): A dictionary containing stocks in the portfolio and their quantities.
            Example: {'AAPL': 10, 'GOOG': 5, 'MSFT': 20}
    """
    industries = {}
    
    for stock, quantity in portfolio.items():
        stock_info = get_stock_info(stock)
        industry = stock_info['info'].get('industry')
        if industry:
            if industry in industries:
                industries[industry] += quantity
            else:
                industries[industry] = quantity
    
    if not industries:
        print("No industry information available for the stocks in the portfolio.")
        return
    
    total_quantity = sum(industries.values())
    
    print("Portfolio Diversification by Industry:")
    for industry, quantity in industries.items():
        percentage = (quantity / total_quantity) * 100
        print(f"- {industry}: {quantity} shares ({percentage:.2f}%)")

       

def portfolio_risk(portfolio):
    """
    This function will evaluate the risk of portfolio by caculating its variance and covariance
    
    Parameters:
        portfolio (list): A list of dictionaries representing the portfolio, where each dictionary contains 'ticker' and 'quantity' keys
        
    Returns:
        tuple: A tuple containing the portfolio variance and covariance
    """
    prices = {}
    for stock in portfolio:
        ticker = stock['ticker']
        quantity = stock['quantity']
        hist = get_stock_info(ticker)['hist']
        prices[ticker] = hist['Close'] * quantity
    
    prices_df = pd.DataFrame(prices)
    returns_df = prices_df.pct_change().dropna()
    
    # Calculate portfolio variance and covariance
    cov_matrix = returns_df.cov()
    var_portfolio = np.dot(weights.T, np.dot(cov_matrix, weights))
    variances = np.diag(cov_matrix.values)
    covariance = []
    for i in range(len(variances)):
        for j in range(i+1, len(variances)):
            cov = cov_matrix.iloc[i,j] * variances[i] * variances[j] ** 0.5
            covariance.append(cov)
    return (var_portfolio, sum(covariance))

import sqlite3

def data_store(portfolio_name, portfolio_return, portfolio_risk, portfolio_diversity):
    """
    Store portfolio information in an SQLite database
    
    Parameters:
        portfolio_name (str): The name of the portfolio
        portfolio_return (float): The return of the portfolio
        portfolio_risk (float): The risk of the portfolio
        portfolio_diversity (dict): A dictionary containing the diversification of the portfolio
        
    Returns:
        None
    """
    # Connect to database
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    
    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS portfolios
                 (name text, return real, risk real, diversity text)''')
    
    # Insert portfolio information into table
    c.execute("INSERT INTO portfolios VALUES (?, ?, ?, ?)", (portfolio_name, portfolio_return, portfolio_risk, str(portfolio_diversity)))
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
