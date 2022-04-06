'''
/**
 * fetch_single_portfolio_detail.py
 * 
 * Fetch the detail associated with an individual portfolio.
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
from apexe3.apexe3 import fetch_individual_portfolio

import pandas as pd

# usernameVal= "usmanbeta@apexe3.com"
# passwordVal = "password"
# portfolioName = "API Portfolio"
# accessToken = ""

usernameVal= "china@plates.com"
passwordVal = "password"
portfolioName = "API 66 ortfolio"
clientId = "apiclient"
# clientSecret = "1972b74b-4e33-46bf-8a80-314ce9ccedef"
clientSecret = "OoGreWDs1TFExNm5rBBLquqSb0cvPxut"

portfolioId = '2320f0de-1ea5-4f55-a9ab-fb5ad312eed6'

def init():
    username = usernameVal
    password = passwordVal
    initialise(clientId, clientSecret, username, password)

if __name__ == "__main__":
    init()
    portfolioDetail = fetch_individual_portfolio(portfolioId)
    print(portfolioDetail)

