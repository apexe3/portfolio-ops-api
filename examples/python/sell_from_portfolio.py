'''
/**
 * sell_from_portfolio.py
 * 
 * Ability to sell all or some of an asset associated with a portfolio. 
 * Use the other API calls to find the relevant portfolioId and portfolioItem.
 * 
 * Disclaimer:
 * APEX:E3 is a financial technology company based in the United Kingdom https://www.apexe3.com
 *  
 * None of this code constitutes financial advice. APEX:E3 is not 
 * liable for any loss resulting from the use of this code or the API. 
 * 
 * This code is governed by The MIT License (MIT)
 * 
 * Copyright (c) 2022 APEX:E3 Team
 * 
 **/
'''

import sys
sys.path.append('..')
from apexe3.apexe3 import initialise
from apexe3.apexe3 import sell_from_portfolio

import pandas as pd

usernameVal= 'Your username email'
passwordVal = 'Your password'
clientId = ''
clientSecret = ''

portfolioId = ''
portfolioItemId = ''

def init():

    username = usernameVal
    password = passwordVal
    initialise(clientId, clientSecret, username, password)

if __name__ == "__main__":
    init()
    result = sell_from_portfolio(portfolioId, portfolioItemId, usernameVal,'BTC','USD','ftx', 0.1)
    print(result)

