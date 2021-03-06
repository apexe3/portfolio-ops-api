'''
/**
 * construct_portfolio
 * 
 * Ability to construct a portfolio using markets 
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
from apexe3.apexe3 import construct_portfolio_with_params

import pandas as pd


usernameVal= 'Your username email'
passwordVal = 'Your password'
clientId = ''
clientSecret = ''

#Enter a name for this portfolio by replacing the "Add a name" value
portfolioName = "Add a name"

#Uncomment assets or add different assets to the portfolioItems array
#Must have enough balance to buy the assets in this array
portfolioItems = [
        {
            'exchange':'ftx',
            'base':'BTC',
            'quote':'USD',
            'amount':0.001,
        },
        # {
        #     'exchange':'ftx',
        #     'base':'ETH',
        #     'quote':'USD',
        #     'amount':1.2,
        # },
        # {
        #     'exchange':'coinbasepro',
        #     'base':'LINK',
        #     'quote':'USD',
        #     'amount':1000,
        # },
        # {
        #     'exchange':'kraken',
        #     'base':'YFI',
        #     'quote':'USD',
        #     'amount':10,
        # },

    ] 

def init():

    username = usernameVal
    password = passwordVal
    initialise(clientId, clientSecret, username, password)

if __name__ == "__main__":
    init()
    result = construct_portfolio_with_params(usernameVal, portfolioName, portfolioItems)
    print(result)

