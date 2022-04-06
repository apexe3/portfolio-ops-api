'''
/**
 * apexe3.py
 * 
 * Wrapper and utility functions for the APEX:E3 portfolio ops API
 * 
 * Disclaimer:
 * APEX:E3 is a financial technology company based in the United Kingdom https://www.apexe3.com
 * None of this code constitutes financial advice. APEX:E3 is not 
 * liable for any loss resulting from the use of this code or the API. 
 * 
 * This code is governed by The MIT License (MIT)
 * 
 * Copyright (c) 2022 APEX:E3 Team
 * 
 **/
'''


import requests
import websocket
import _thread
import time
import json
import urllib.parse
from operator import itemgetter
import base64
import ssl

authUrl = 'http://localhost/auth/realms/ApexE3/protocol/openid-connect/token'
revolutionsApiUrl  = "http://localhost"
revolutionsApiUrl2  = "https://dev.apexe3.ai"
accessToken = ""


'''
  /**
   * Authenticates and retrieves the autentication token used by subsequent calls 
   * 
   * @param {*} clientId 
   * @param {*} clientSecret
   * @param {*} username
   * @param {*} password 
   */
'''
def initialise(clientId, clientSecret, username, password):
    global accessToken
    accessToken = obtain_access_token(clientId, clientSecret, username, password)
    if(accessToken==''):
        print('Problem with credentials')
        return None
    else:
        print('Credentials ok')
    #initialise_assetId_to_cannoicalId()
    return accessToken

   

'''
    /**
    * Uses the supplied parameters to authenticate and obtain a valid JWT token
    * 
    * @param {*} clientId 
    * @param {*} clientSecret
    * @param {*} username
    * @param {*} password  
    */
'''
def obtain_access_token(clientId, clientSecret, username, password):
    print("--------- Authenticating ---------\n\n")
    data = {
        'grant_type': (None, 'password'),
        'client_id': (None, clientId),
        'client_secret': (None, clientSecret),
        'scope': 'openid',
        'username' : (None, username),
        'password' : (None, password)
    }
    r = requests.post(authUrl, data)
    result = r.json()

    if 'access_token' in result:
        accessToken = result['access_token']
        if accessToken:
            print("--------- Authentication Token Recieved ---------\n\n")
            print(accessToken)
            print("\n\n")
            return accessToken
        else:
            print(
                "--------- Authentication Token Not Recieved. Check creds ---------\n\n")
            return ""
    else:
        print("--------- Authentication Token Not Recieved. Check creds ---------\n\n")
        return ""

'''
    /**
    * 
    * Calls the API based on the spec defined in:
    * https://api.ae3platform.com/docs#tag/Reference
    * 
    * @param {*} endpointUrlPart 
    */
'''
def fetch_reference_data(endpointUrlPart):
    global accessToken

    referenceListUrl = requestApiUrl + endpointUrlPart
    headers = {
        'Authorization': 'bearer ' + accessToken,
        'Content-Type': 'application/json'
    }
    references = requests.get(referenceListUrl, headers=headers)
    if(references and 'result' in references.json()):
        return references.json()['result']
    else:
        return "references not found"



def construct_portfolio(portfolioParams):
    global accessToken

    headers = {
        'Authorization': 'bearer ' + accessToken,
        'Content-Type': 'application/json'
    }
    portfolio = portfolioParams['portfolio']
    portfolioItems = portfolioParams['portfolioItems']

    portfolios = []
    portfolios.append(portfolio)

    balance  = fetch_balance()
    balance = float(balance['balance'])

    portFoliolPosturl = revolutionsApiUrl+'/portfolio'
    portfolioId = requests.post(portFoliolPosturl, data=json.dumps(portfolios),headers=headers)

    portfolioId = portfolioId.json()[0]['portfolioId']

    portfolioItemsToSend = []

    totalValue = 0
    for pItem in portfolioItems:
        portfolioItem = {}
        portfolioItem['id'] = 'x'
        portfolioItem['ownerId'] = portfolio['ownerId']
        portfolioItem['portfolioId'] = portfolioId
        portfolioItem['venue'] = pItem['exchange']
        portfolioItem['symbol'] = pItem['base']+'/'+pItem['quote']
        portfolioItem['type'] = 'MARKET'
        portfolioItem['base'] = pItem['base']
        portfolioItem['quote'] = pItem['quote']
        portfolioItem['blockchainType'] = ''
        portfolioItem['tokenAddress'] = ''
        portfolioItem['amount'] = pItem['amount']
        portfolioItem['startingPrice'] = fetch_price_for_market(pItem['exchange'],pItem['base'],pItem['quote'])['c']
        portfolioItem['initialValue'] = portfolioItem['startingPrice'] * portfolioItem['amount']
        totalValue = totalValue + (portfolioItem['startingPrice'] * portfolioItem['amount'])
        portfolioItem['currentPrice'] = -1
        portfolioItem['currentValue'] = -1
        portfolioItem['roiPercent'] = -1
        portfolioItem['createdAt'] = ''
        portfolioItemsToSend.append(portfolioItem)
    
    if(totalValue>balance):
        return 'Not enough balance because your balance is ' + str(balance) + ' and value of the portfolio is ' + str(totalValue)

    portFoliolPosturl = revolutionsApiUrl+'/portfolio-item'
    portfolioIds = requests.post(portFoliolPosturl, data=json.dumps(portfolioItemsToSend),headers=headers)     

    result = {'portfolioId': portfolioId, 'portfolioItemIds':portfolioIds.json()}
    return result


def fetch_portfolio_for_id(ownerId,id):
    global accessToken

    portfolioIdsUrl = revolutionsApiUrl+'/portfolio-view/portfolio/'+ownerId+'/'+id
    headers = {
        'Authorization': 'bearer ' + accessToken,
        'Content-Type': 'application/json'
    }
    portfolio = requests.get(portfolioIdsUrl, headers=headers)

    return portfolio.json()

def fetch_balance():
    global accessToken

    myBalanceUrl = revolutionsApiUrl+'/entity/my-balance'
    headers = {
        'Authorization': 'bearer ' + accessToken,
        'Content-Type': 'application/json'
    }
    myBalance = requests.get(myBalanceUrl, headers=headers)

    return myBalance.json()

def fetch_supported_markets(exchange):
    global accessToken

    instrumentsUrl = revolutionsApiUrl+'/instruments/supported-markets/'+exchange
    headers = {
        'Authorization': 'bearer ' + accessToken,
        'Content-Type': 'application/json'
    }
    
    instruments = requests.get(instrumentsUrl, headers=headers)

    return instruments.json()

def fetch_my_portfolios():
    global accessToken

    myPortfoliosUrl = revolutionsApiUrl+'/portfolio-view/my-portfolios'
    headers = {
        'Authorization': 'bearer ' + accessToken,
        'Content-Type': 'application/json'
    }
    
    myPortfolios = requests.get(myPortfoliosUrl, headers=headers)

    return myPortfolios.json()
    
def fetch_individual_portfolio(portfolioId):
    global accessToken

    individualPortfolioUrl = revolutionsApiUrl+'/portfolio-view/individual/'+portfolioId
    headers = {
        'Authorization': 'bearer ' + accessToken,
        'Content-Type': 'application/json'
    }
    
    individualPortfolio = requests.get(individualPortfolioUrl, headers=headers)

    return individualPortfolio.json()


'''
  /**
  * fetch a price
  *
  */ 
'''  
def fetch_price_for_market(exchange,base,quote):
    global accessToken

    priceUrl = revolutionsApiUrl2+'/portfolio-view/current-price/'+exchange+'/'+base+'/'+quote
    headers = {
        'Authorization': 'bearer ' + accessToken,
        'Content-Type': 'application/json'
    }
    price = requests.get(priceUrl, headers=headers)

    return price.json() 

def sell_from_portfolio(portfolioId, portfolioItemId, ownerId, base,quote,venue, amount):
    balance  = fetch_balance()
    if('balance' in balance):
        print('Your balance is ',float(balance['balance']))
        balance = float(balance['balance'])
    else:
        print('could not fetch balance')
        return 'could not fetch bslance'

    price = fetch_price_for_market(venue,base,quote)['c']
    value = float(price) * float(amount)

    trade = {
        'portfolioId':portfolioId,
        'portfolioItemId' : portfolioItemId,
        'ownerId' : ownerId,
        'venueId' : venue,
        'base' : base,
        'quote' : quote,
        'unitAmountSold' : amount,
        'valueAmountSold' : (amount * price),
        'boughtAtMs' : 0,
        'soldAtPrice' : price,
        'createdBy' : ownerId
    }

    portFoliolItemSellPosturl = revolutionsApiUrl+'/trade'

    headers = {
        'Authorization': 'bearer ' + accessToken,
        'Content-Type': 'application/json'
    }

    result = requests.post(portFoliolItemSellPosturl, data=json.dumps([trade]),headers=headers)
    return result.json()



def add_to_portfolio(portfolioId, ownerId, base,quote,venue, amount):
    balance  = fetch_balance()

    if('balance' in balance):
        print('Your balance is ',float(balance['balance']))
        balance = float(balance['balance'])
    else:
        print('could not fetch balance')
        return 'could not fetch bslance'

    price = fetch_price_for_market(venue,base,quote)['c']
    value = float(price) * float(amount) 

    if(value > balance):
        print('Not enought balance')
        return 'Not enough balance'


    portfolioItemToUpdate = {'portfolioId' : portfolioId,
        'ownerId' : ownerId,
        'amount' : float(amount),
        'symbol' : base+'/'+quote,
        'venue' : venue,
        'base' : base,
        'quote' : quote,
        'type' : 'CRYPTO',
        'createdBy' :ownerId
    }

    portFoliolItemPosturl = revolutionsApiUrl+'/portfolio-item'

    headers = {
        'Authorization': 'bearer ' + accessToken,
        'Content-Type': 'application/json'
    }

    result = requests.post(portFoliolItemPosturl, data=json.dumps([portfolioItemToUpdate]),headers=headers)
    return result.json()





def construct_portfolio_with_params(usernameVal, portfolioName, portfolioItems):
    portfolioParams = {

        'portfolio': {
            'portfolioId':'x',
            'ownerId': usernameVal,
            'portfolioName': portfolioName,
            'imageLink':'https://portfolio-image',
            'startingBalanceUSD': 0,
            'remainingBalanceUSD' : 0,
            'initialTotalValue' : 0,
            'currentTotalValue' : 0,
            'totalROIPercent' : 0,
            'createdAt':''
            },

        'portfolioItems': portfolioItems

    }

    balance  = fetch_balance()
    print('Your balance is ',float(balance['balance']))

    result = construct_portfolio(portfolioParams)
    
    if(result!='' and result!=None):
        print('Make a note of the portfolio id. Save this somewhere if you would like to addTo or sellFrom this portfolio: ')
        print(result)
    
    if 'portfolioId' in result: 
        portfolioId = result['portfolioId']
        if(portfolioId):
            evaluatedPortfolio = fetch_portfolio_for_id(usernameVal, portfolioId)
            return(evaluatedPortfolio)
        else:
            return('Could not get portfolio. It is likely you do not have enough balance')
    else:
        return('Could not get portfolio. It is likely you do not have enough balance')  
