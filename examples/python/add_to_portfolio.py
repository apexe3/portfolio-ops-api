'''
/**
 * add_to_portfolio.py
 * 
 * Add an asset to an existing portfolio. 
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
from apexe3.apexe3 import add_to_portfolio

import pandas as pd

usernameVal= 'Your username email'
passwordVal = 'Your password'
clientId = ''
clientSecret = ''

portfolioId = ''

def init():

    username = usernameVal
    password = passwordVal
    initialise(clientId, clientSecret, username, password)

if __name__ == "__main__":
    init()
    
    result = add_to_portfolio(portfolioId, usernameVal, 'BTC','USD','ftx', 0.01)
    print('Use this portfolioItemId when selling')
    print(result)

