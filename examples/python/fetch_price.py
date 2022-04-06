'''
/**
 * fetch_price.py
 * 
 * Fetch price for an individual market. Use the supported markets API endpoint
 * to get relevant market id's and information. 
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
from apexe3.apexe3 import fetch_price_for_market

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
    price = fetch_price_for_market('ftx','BTC','USD')
    print(price)

