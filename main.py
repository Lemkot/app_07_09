# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 21:40:41 2020

@author: win10
"""

# 1. Library imports
import uvicorn
from fastapi import FastAPI
#import numpy as np
import json5
from fastapi.logger import logger
import yfinance as yf
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

# 2. Create the app object
app = FastAPI()

@app.get('/')
async def price():
    try:        
        # Define the ticker symbol of the stock you want to fetch data for
        ticker_symbol = 'AAPL'
        
        # Create a Yahoo Finance ticker object
        stock = yf.Ticker(ticker_symbol)
        
        # Fetch historical data for the stock
        historical_data = stock.history(period='1y')  # Adjust the period as needed
        
        # Extract the most recent closing price
        prices = historical_data['Close']
        
        # Fit an ARIMA model to the training data
        order = (5, 1, 0)  # Example order for ARIMA (p, d, q)
        model = ARIMA(prices, order=order)
        model_fit = model.fit()
        
        # Forecast the next day's price
        forecasted_value_next_day = model_fit.forecast(steps=1).iloc[0]
        
        return {"forecasted_price": float(forecasted_value_next_day)}

    except Exception as e:
        return {"error": str(e)}

    

# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    
#uvicorn app:app --reload
