'''
/**
 * fetch_my_portfolio_summaries.py
 * 
 * Fetches all your portfolio summaries. The portfolioIds in the result set 
 * cam be used to get more detauls via the other API calls. 
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
from apexe3.apexe3 import fetch_my_portfolios

import pandas as pd

usernameVal= 'Your username email'
passwordVal = 'Your password'
clientId = ''
clientSecret = ''

def init():

    username = usernameVal
    password = passwordVal
    initialise(clientId, clientSecret, username, password)

if __name__ == "__main__":
    init()
    # exchanges values: ftx  coinbasepro  kraken
    portfolios = fetch_my_portfolios()
    print(portfolios)

