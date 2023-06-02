import okex.Trade_api as Trade
import requests, time

api_key = ""
secret_key = ""
passphrase = ""
instId = "ETH-USDC"
flag = '0'

tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)

while True:
    try:
        ticker = requests.get('http://www.okex.com/api/v5/market/ticker?instId=BTC-USDC').json()
        print(ticker['data'][0]['bidPx'])
    except Exception as e:
        print(f'Unable to obtain ticker: {e}')
    
    if float(ticker['data'][0]['bidPx']) >= 32000.00:
        try: 
           result = tradeAPI.place_order(instId=instId, tdMode='cash', side='buy',
                                           ordType='limit', sz='0.005', px='2000.00')
           ordId = result['data'][0]['ordId']
        except Exception as e:
            print(f'Unable to execute order: {e}')

        time.sleep(2)

        try:
            check = tradeAPI.get_orders(instId, ordId)
        except Exception as e:
            print(f'Unable to check order: {e}')

        if check['data'][0]['state'] == 'canceled':
            print('Order was canceled.')
            break
        else:
            print('Order was executed!')
            break 
    else:
        print('Requirement not reached.')
        time.sleep(15)