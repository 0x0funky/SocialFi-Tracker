import streamlit as st
import pandas as pd
import time
import datetime
import requests
from web3 import Web3
import tweepy
import brotli
import json
import base64
from datetime import timedelta

# Twitter API credentials
API_KEY = st.secrets["API_KEY"]
API_SECRET_KEY = st.secrets["API_SECRET_KEY"]
ACCESS_TOKEN = st.secrets["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = st.secrets["ACCESS_TOKEN_SECRET"]
NBC_Barear = st.secrets["NBC_Barear"]
SA_Barear = st.secrets["SA_Barear"]
SA_API_KEY = st.secrets["SA_API_KEY"]
FT_API_KEY = st.secrets["FT_API_KEY"]




# Authenticate with Twitter
auth = tweepy.OAuth1UserHandler(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
)

api = tweepy.API(auth)

def get_user_details(username):
    user = api.get_user(screen_name=username)

    followers_count = user.followers_count
    tweets_count = user.statuses_count
    
    return {
        "followers_count": followers_count,
        "tweets_count": tweets_count,
        "latest_tweet_retweet_count": None
    }

st.set_page_config(page_title= "SocialFi-Tracker", page_icon="./SocialFi_Tracker.png", layout="wide")

def fetch_player_profile_FT_user(twt_username):
    url = f"https://prod-api.kosetto.com/twitter-users/{twt_username}"

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "If-None-Match": 'W/"393-bQFpAMnh8Hty9ncnU1mwsiSXI/8"',
        "Origin": "https://www.friend.tech",
        "Referer": "https://www.friend.tech/",
        "Sec-Ch-Ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        return data
#         return str(float(data["displayPrice"])/1e18)
#         print(data)
    else:
#         print(f"Request failed with status code: {response.status_code}")
        return "No Data"

def fetch_player_profile_FT_address(address):
    url = f"https://prod-api.kosetto.com/users/{address}"

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "If-None-Match": 'W/"393-bQFpAMnh8Hty9ncnU1mwsiSXI/8"',
        "Origin": "https://www.friend.tech",
        "Referer": "https://www.friend.tech/",
        "Sec-Ch-Ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        return data
#         return str(float(data["displayPrice"])/1e18)
#         print(data)
    else:
#         print(f"Request failed with status code: {response.status_code}")
        return "No Data"


def get_user_NBC_data(user_name):
    url = "https://alpha-api.newbitcoincity.com/api/player-share/tokensv1"
    headers = {
        "Authorization": f"Bearer {NBC_Barear}",
    }

    # for i in range(41,60):
        # Define the parameters
    params = {
        "network": "nos",
        "page": 1,
        "limit": 1,
        "key_type": 1,
        "side": 1,
        "address": "0x58264Ac8e24a101ef90b28616C740863b159083b",
        "followers": "0,200000",
        "holder": 0,
        "placeholder": 0,
        "price": "0,1000",
        "search":f"{user_name}"
    }
    response = requests.get(url, headers=headers, params=params)
    try:
        data = response.json()
        return data["result"]
    except Exception as e:
        print ("error:"+ str(e))
    

def get_user_SA_data(handle):
    BASE_URL = "https://api.starsarena.com/user/handle"
    HEADERS = {
        "Accept": "application/json",
        "Authorization": f"Bearer {SA_Barear}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    }

    response = requests.get(f"{BASE_URL}?handle={handle}", headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()['user']
    else:
        return {"error": "Failed to fetch data"}

def get_SA_price(user_address):
    user_address = Web3.toChecksumAddress(user_address)
    w3 = Web3(Web3.HTTPProvider('https://api.avax.network/ext/bc/C/rpc'))
    true = True
    false = False

    contract_address = '0x563395A2a04a7aE0421d34d62ae67623cAF67D03'
    contract_abi = [{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"version","type":"uint8"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"address","name":"referrer","type":"address"}],"name":"ReferralSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"trader","type":"address"},{"indexed":false,"internalType":"address","name":"subject","type":"address"},{"indexed":false,"internalType":"bool","name":"isBuy","type":"bool"},{"indexed":false,"internalType":"uint256","name":"shareAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"protocolAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"subjectAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"referralAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"supply","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"buyPrice","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"myShares","type":"uint256"}],"name":"Trade","type":"event"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"allowedTokens","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"buyShares","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"referrer","type":"address"}],"name":"buySharesWithReferrer","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getBuyPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getBuyPriceAfterFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"}],"name":"getMyShares","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"subject","type":"address"},{"internalType":"uint256","name":"supply","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getSellPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getSellPriceAfterFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"}],"name":"getSharesSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"initialPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_subject","type":"address"},{"internalType":"address[]","name":"_traders","type":"address[]"},{"internalType":"uint256[]","name":"_amounts","type":"uint256[]"}],"name":"migrateTickets","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"pendingTokenWithdrawals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"pendingWithdrawals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"protocolFeeDestination","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"protocolFeeDestination2","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"protocolFeePercent","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"referralFeePercent","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"revenueShare","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"sellShares","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"referrer","type":"address"}],"name":"sellSharesWithReferrer","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_feeDestination","type":"address"}],"name":"setFeeDestination","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_feeDestination2","type":"address"}],"name":"setFeeDestination2","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_paused","type":"bool"}],"name":"setPaused","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_feePercent","type":"uint256"}],"name":"setProtocolFeePercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_feePercent","type":"uint256"}],"name":"setReferralFeePercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_feePercent","type":"uint256"}],"name":"setSubjectFeePercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"shareholders","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"sharesBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"sharesSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"subjectFeePercent","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"subscribers","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"subscriptionDuration","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"subscriptionPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"subscriptionTokenAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"subscriptionsEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userToReferrer","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"weightA","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"weightB","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"weightC","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"weightD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]  # Replace with the ABI you got from Snowtrace

    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    supply_result = contract.functions.getSharesSupply(user_address).call()
    SA_price = contract.functions.getBuyPrice(user_address,1).call()
    return supply_result, SA_price/1e18


def SA_balance(address):
    BASE_URL = "https://api.snowtrace.io/api"
    PARAMS = {
        "module": "account",
        "action": "txlist",
        "address": f"{address}",
        "startblock": 35000000,
        "endblock": 40000000,
        "page": 1,
        "offset": 10000,
        "sort": "asc",
        "apikey": SA_API_KEY  # Replace with your actual API key
    }

    # Make the request
    response = requests.get(BASE_URL, params=PARAMS)
    data = response.json()
    return data['result']


def SA_in_out_balance(data, address):
    # address = address
    transactions = data
    # total_out_value =  sum(int(tx['value']) for tx in transactions if ((tx['from'].lower() == address.lower()) and (tx["to"].lower!="0x563395A2a04a7aE0421d34d62ae67623cAF67D03".lower())))
    total_incoming_value = 0
    total_incoming_value1 = sum(int(tx['value']) for tx in transactions if (tx['to'].lower() == address.lower()) and (tx['from'].lower() != address.lower()))
    total_out_value = 0
    total_out_value1 = 0
    for tx in transactions:
        if tx['to'].lower() == address.lower():
            pre_address = tx["from"]
            if pre_address.lower() =="0xA16F524a804BEaED0d791De0aa0b5836295A2a84".lower():
                break
            if pre_address.lower() =="0x9f8c163cBA728e99993ABe7495F06c0A3c8Ac8b9".lower():
                break
            transactions2 = SA_balance(pre_address)
            total_incoming_value = sum(int(tx2['value']) for tx2 in transactions2 if (tx2['to'].lower() == pre_address.lower()) and (tx2['to'].lower() != address.lower()) and (tx2['from'].lower() != pre_address.lower()))
            total_out_value1 =  sum(int(tx2['value']) for tx2 in transactions2 if ((tx2['from'].lower() == pre_address.lower()) and (tx2['to'].lower() != pre_address.lower()) and (tx2["to"].lower() !="0xA481B139a1A654cA19d2074F174f17D7534e8CeC".lower()) and (tx2["to"].lower() != address.lower())))
            total_out_value =  sum(int(tx['value']) for tx in transactions if ((tx['from'].lower() == address.lower()) and (tx['to'].lower() != address.lower()) and (tx["to"].lower()!="0x563395A2a04a7aE0421d34d62ae67623cAF67D03".lower()) and (tx["to"].lower()!=pre_address.lower())))
            break

    # total_out_value/1e18, total_out_value1/1e18
            
    return (total_incoming_value1+total_incoming_value)/1e18, (total_out_value+total_out_value1)/1e18


def fetch_wbtc_buy_history(address):
    url = f"https://api.trustlessbridge.io/api/wbtc-buy-history?address={address}"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://newbitcoincity.com",
        "Referer": "https://newbitcoincity.com/",
        "Authorization": "Bearer null",  # This seems to be a placeholder, adjust if needed
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        total_amount = 0
        for i in data['data']:
            try:
                total_amount+=float(i["actualToAmount"])
            except:
                continue
        return total_amount/1e18
    else:
        response.raise_for_status()

def NBC_tx(addressHash):
# addressHash = "0x1b23a52d3bba7ed9bb30a35e50b61f7be5ec7f0c"
    BASE_URL = f"https://explorer.l2.trustless.computer/api?module=account&action=txlist&address={addressHash}&offset=10000"
    # Make the request
    response = requests.get(BASE_URL)
    data = response.json()
    transactions = data["result"]
    return transactions


def NBC_withdraw(addressHash):
    BASE_URL = f"https://explorer.l2.trustless.computer/api?module=account&action=txlist&address={addressHash}&offset=10000"
    # Make the request
    response = requests.get(BASE_URL)
    data = response.json()
    transactions = data["result"]
    true = True
    false = False

    ABI = [{"type":"event","name":"BridgeToken","inputs":[{"type":"address","name":"token","internalType":"contract WrappedToken","indexed":false},{"type":"address","name":"burner","internalType":"address","indexed":false},{"type":"uint256","name":"amount","internalType":"uint256","indexed":false},{"type":"string","name":"extddr","internalType":"string","indexed":false},{"type":"uint256","name":"destChainId","internalType":"uint256","indexed":false}],"anonymous":false},{"type":"event","name":"Initialized","inputs":[{"type":"uint8","name":"version","internalType":"uint8","indexed":false}],"anonymous":false},{"type":"event","name":"Mint","inputs":[{"type":"address[]","name":"tokens","internalType":"contract WrappedToken[]","indexed":false},{"type":"address[]","name":"recipients","internalType":"address[]","indexed":false},{"type":"uint256[]","name":"amounts","internalType":"uint256[]","indexed":false}],"anonymous":false},{"type":"event","name":"Mint","inputs":[{"type":"address","name":"token","internalType":"contract WrappedToken","indexed":false},{"type":"address[]","name":"recipients","internalType":"address[]","indexed":false},{"type":"uint256[]","name":"amounts","internalType":"uint256[]","indexed":false}],"anonymous":false},{"type":"event","name":"OwnershipTransferred","inputs":[{"type":"address","name":"previousOwner","internalType":"address","indexed":true},{"type":"address","name":"newOwner","internalType":"address","indexed":true}],"anonymous":false},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"contract IERC20"}],"name":"ETH_TOKEN","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"bridgeToken","inputs":[{"type":"address","name":"token","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"},{"type":"string","name":"externalAddr","internalType":"string"},{"type":"uint256","name":"destChainId","internalType":"uint256"}]},{"type":"function","stateMutability":"payable","outputs":[],"name":"bridgeToken","inputs":[{"type":"string","name":"externalAddr","internalType":"string"},{"type":"uint256","name":"destChainId","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"burnableToken","inputs":[{"type":"address","name":"","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"initialize","inputs":[{"type":"address","name":"safeMultisigContractAddress","internalType":"address"},{"type":"address","name":"operator_","internalType":"address"},{"type":"address[]","name":"tokens","internalType":"address[]"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"mint","inputs":[{"type":"address[]","name":"tokens","internalType":"contract WrappedToken[]"},{"type":"address[]","name":"recipients","internalType":"address[]"},{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"mint","inputs":[{"type":"address","name":"token","internalType":"contract WrappedToken"},{"type":"address[]","name":"recipients","internalType":"address[]"},{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"operator","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"owner","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"renounceOwnership","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"transferOperator","inputs":[{"type":"address","name":"operator_","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"transferOwnership","inputs":[{"type":"address","name":"newOwner","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"updateToken","inputs":[{"type":"address[]","name":"tokens","internalType":"address[]"},{"type":"bool[]","name":"isBurns","internalType":"bool[]"}]}]


    w3 = Web3()

    contract = w3.eth.contract(abi=ABI)
    output_amount = 0
    try:
        for i in transactions:
            if i["to"].lower() == "0x966d0714eFA3e3950A2bd4F4b3760D0Fc07209f5".lower():
                input_data = i["input"]
                decoded_data = contract.decode_function_input(input_data)
                output_amount+=decoded_data[1]['amount']
    #             print (decoded_data[1]['amount']/1e18)
        return (output_amount/1e18)
    except:
        return 0


def FT_balance_tx(address):
# Define the API endpoint and parameters
    BASE_URL = "https://api.basescan.org/api"
    PARAMS = {
        "module": "account",
        "action": "txlist",
        "address": f"{address}",
        "startblock": 2000000,
        "endblock": 6000000,
        "page": 1,
        "offset": 10000,
        "sort": "asc",
        "apikey": FT_API_KEY  # Replace with your actual API key
    }

    # Make the request
    response = requests.get(BASE_URL, params=PARAMS)
    data = response.json()
    return data['result']

def FT_balance_itx(address):
# Define the API endpoint and parameters
    BASE_URL = "https://api.basescan.org/api"
    PARAMS = {
        "module": "account",
        "action": "txlistinternal",
        "address": f"{address}",
        "startblock": 2000000,
        "endblock": 6000000,
        "page": 1,
        "offset": 10000,
        "sort": "asc",
        "apikey": FT_API_KEY  # Replace with your actual API key
    }

    # Make the request
    response = requests.get(BASE_URL, params=PARAMS)
    data = response.json()
    return data['result']

def FT_buy_sell_count(data, time_hours):
    buy_count = 0
    sell_count = 0
    for i in data:
        if ("0xb51d0534" in i["input"]) and is_within_last_hours(int(i["timeStamp"]), time_hours):
            sell_count+=1
        if "0x6945b123" in i["input"] and is_within_last_hours(int(i["timeStamp"]), time_hours):
            buy_count+=1
    return buy_count, sell_count

def NBC_buy_sell_count(data, time_hours):
    buy_count = 0
    sell_count = 0
    for i in data:
        if ("0x3f566994" in i["input"]) and is_within_last_hours(int(i["timeStamp"]), time_hours):
            sell_count+=1
        if "0x74567f0f" in i["input"] and is_within_last_hours(int(i["timeStamp"]), time_hours):
            buy_count+=1
    return buy_count, sell_count

def SA_buy_sell_count(data, time_hours):
    buy_count = 0
    sell_count = 0
    for i in data:
        if (("0xaac35d87" in i["input"]) or ("0xb51d0534" in i["input"])) and is_within_last_hours(int(i["timeStamp"]), time_hours):
            sell_count+=1
        if (("0x6945b123" in i["input"]) or ("0xe9ccf3a3" in i["input"])) and is_within_last_hours(int(i["timeStamp"]), time_hours):
            buy_count+=1
    return buy_count, sell_count

# Test the function

# address_value = "0x58264ac8e24a101ef90b28616c740863b159083b"

# data = fetch_player_profile_NBC(address_value)
# # data = fetch_player_profile_FT_address(address_value)
# print(data)

UPDATE_INTERVAL = 5  # in seconds


# current_account_info = pd.read_csv("NBC_Accounts.csv")
# list_user = current_account_info["user_twitter_username"].tolist()

def process_input(user_input):
    # print (user_input)
    try:
        user_json = get_user_details(user_input)
    except:
        user_json = {
            "followers_count": None,
            "tweets_count": None,
            "latest_tweet_retweet_count": None
        }
    data = fetch_player_profile_FT_user(user_input)
    if data == "No Data":
        # FT_str = f"FT => No Data"
        pfp_link = ""
        price_FT = "None"
        supply_share = "None"
        FT_address = "None"
        FT_in_all = "None"
        FT_out_all = "None"
        FT_data = None
    else:
        pfp_link = data["twitterPfpUrl"]
        price_FT = float(data["displayPrice"])/1e18
        supply_share = int(data["shareSupply"])
        FT_address = data["address"]
        data = FT_balance_tx(FT_address)
        FT_data = data
        transactions = data
        total_out_value = sum(int(tx['value']) for tx in transactions if ((tx['from'].lower() == FT_address.lower()) and (tx["to"].lower()!="0xCF205808Ed36593aa40a44F10c7f7C2F67d4A4d4".lower())))
        total_incoming_value1 = sum(int(tx['value']) for tx in transactions if (tx['to'].lower() == FT_address.lower() and tx['from'].lower() != FT_address.lower()))
        data = FT_balance_itx(FT_address)
        transactions = data
        total_incoming_value = sum(int(tx['value']) for tx in transactions if (tx['to'].lower() == FT_address.lower()) and (tx['from'].lower()!="0xCF205808Ed36593aa40a44F10c7f7C2F67d4A4d4".lower()) and (tx['from'].lower()!=FT_address.lower()))
        
        FT_in_all = (total_incoming_value1+total_incoming_value)/1e18
        FT_out_all = total_out_value/1e18

    SA_data = get_user_SA_data(user_input)
    if SA_data:
        if pfp_link == "":
            pfp_link = SA_data["twitterPicture"]
        SA_address = SA_data["address"]
        supply_share_SA, price_SA = get_SA_price(SA_address)
        SA_data = SA_balance(SA_address)
        SA_in_all, SA_out_all = SA_in_out_balance(SA_data, SA_address)
    else:
        SA_address = "None"
        supply_share_SA = "None"
        price_SA = "None"
        SA_in_all = "None"
        SA_out_all = "None"
        SA_data = None


    NBC_data = get_user_NBC_data(user_input)
        # FT_str = f"FT => Price: {price_FT} ETH, ShareSupply: {supply_share}"
    if (len(NBC_data)>0) and (NBC_data[0]["user_twitter_username"].lower() == user_input.lower()):
        NBC_address = NBC_data[0]['owner']
        price_NBC = float(NBC_data[0]["price"])
        supply_share_NBC = float(NBC_data[0]["total_supply"])
        NBC_data = NBC_tx(NBC_address)
        NBC_in_all = fetch_wbtc_buy_history(NBC_address)
        NBC_out_all = NBC_withdraw(NBC_address)
        if pfp_link == "":
            pfp_link = NBC_data[0]["user_twitter_avatar"]
    else:
        price_NBC = "None"
        NBC_address = "None"
        supply_share_NBC = "None"
        NBC_in_all = "None"
        NBC_out_all = "None"
        NBC_data = None



        # NBC_str = f"NBC => Price: {price_NBC} BTC, ShareSupply: {supply_share_NBC}"
    
    # reply_str=f"""0x0funky || {FT_str} || {NBC_str} """
    # print (f"FT address = {FT_address}")
    # print (f"SA address = {SA_address}")
    # print (f"NBC address = {NBC_address}")

    # For demonstration purposes, I'll just generate some mock data based on the user input.
    image_path = pfp_link  # replace with path to your image
    hyperlink = f"https://twitter.com/{user_input}"  # replace with your hyperlink
    values = [price_FT, supply_share, price_NBC, supply_share_NBC, price_SA, supply_share_SA]
    wallet_list = [FT_address, NBC_address, SA_address, NBC_address]
    in_list = [FT_in_all, NBC_in_all, SA_in_all, NBC_in_all]
    out_list = [FT_out_all, NBC_out_all, SA_out_all, NBC_out_all]
    data_list = [FT_data, NBC_data, SA_data, SA_data]
    return image_path, hyperlink, values, wallet_list, user_json, in_list, out_list, data_list

# st.title("SocialFi Tracker")


def image_to_base64(img_path):
    with open(img_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

icon_url = f"data:image/png;base64,{image_to_base64('./SocialFi_Tracker.png')}"
title_text = "SocialFi Tracker"

st.markdown(f'<img src="{icon_url}" style="vertical-align:middle; display:inline; margin-right:10px; width:40px; height:40px;"> <span style="font-size: 45px; vertical-align:middle;"><strong>{title_text}</strong></span>', unsafe_allow_html=True)
st.write("Eazy to know the price, supply, deposit across the 4 popular SocialFi")

current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
st.write("Last updated:", current_time)


# auto_update = st.checkbox('Auto update every 10 seconds', value=False)
user_input = st.text_input("Enter Twitter User Name:")


def is_within_last_hours(timestamp, hour):
    # Convert the timestamp to a datetime object
    dt_object = datetime.datetime.utcfromtimestamp(timestamp)
    
    # Get the current UTC time
    current_time = datetime.datetime.utcnow()
    
    # Subtract 7 hours from the current time
    seven_hours_ago = current_time - timedelta(hours=hour)
    
    # Check if the timestamp is within the last 7 hours
    return dt_object > seven_hours_ago

def update_data(data, plat, hours):
    if data:
        if plat == "FT":
            buy_count, sell_count = FT_buy_sell_count(data, hours)
        if plat == "SA":
            buy_count, sell_count = SA_buy_sell_count(data, hours)
        if plat == "NBC":
            buy_count, sell_count = NBC_buy_sell_count(data, hours)
        # Your data fetching and processing logic here.
        # Use the 'hours' variable to adjust your data fetching as needed.
        st.write(f"Buy tx in {hours} hours: ", buy_count)
        st.write(f"Sell tx in {hours} hours: ", sell_count)
    else:
        st.write(f"Buy tx in {hours} hours: ", "None")
        st.write(f"Sell tx in {hours} hours: ", "None")

if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

if 'userchange' not in st.session_state:
    st.session_state.userchange = None

rerun_flag = False

if user_input:

    
    price_AVAX_response = requests.get(f"https://api.snowtrace.io/api?module=stats&action=ethprice&apikey={SA_API_KEY}")
    price_AVAX = float(price_AVAX_response.json()["result"]["ethusd"])
    price_ETH_response = requests.get(f"https://api.basescan.org/api?module=stats&action=ethprice&apikey={FT_API_KEY}")
    price_ETH = float(price_ETH_response.json()["result"]["ethusd"])
    price_BTC = price_ETH/float(price_ETH_response.json()["result"]["ethbtc"])
    st.write("Current price: ", f"ETH = {round(price_ETH,3)} USD, ", f"BTC = {round(price_BTC,3)} USD, ", f"AVAX = {round(price_AVAX,3)} USD")
    if (st.session_state.userchange != user_input) or rerun_flag:
        # image, link, vals, wall_list, user_json, in_list, out_list = process_input(user_input)
        with st.spinner('Wait for it...'):
            st.session_state.processed_data = process_input(user_input)
        st.session_state.userchange = user_input
        image, link, vals, wall_list, user_json, in_list, out_list, data_list = st.session_state.processed_data
    else:
        image, link, vals, wall_list, user_json, in_list, out_list, data_list = st.session_state.processed_data

    col1, col2, col3, col4, col5 = st.columns(5)

    # Display image
    with col1:
        # st.image(image, caption="user_input", use_column_width=True)
        X_image = "https://about.twitter.com/content/dam/about-twitter/x/brand-toolkit/logo-black.png.twimg.1920.png"
        if image =="":
            link = "https://twitter.com/"
            image = X_image
        # Display image with hyperlink
        # st.markdown(f"[![Your Image]({image})]({link})")
        st.markdown(f'<a href="{link}" target="_blank"><img src="{image}" width="100%"></a>', unsafe_allow_html=True)
        st.markdown(f"**@{user_input}**")
        st.markdown(f"**Followers:** <span style='font-size: 18px;'>{user_json['followers_count']}</span>", unsafe_allow_html=True)
        st.markdown(f"**Tweets counts:** <span style='font-size: 18px;'>{user_json['tweets_count']}</span>", unsafe_allow_html=True)

    with col2:

        # col11, col21 = st.columns(2)
        FT_image = "https://forkast.news/wp-content/uploads/2023/08/Friend.tech-logo-1260x709.jpeg"
        FT_url = f"https://www.friend.tech/{user_input}"

        FT_price = vals[0]
        if FT_price == "None":
            FT_price_u = "None"
        else:
            FT_price_u = round(FT_price*price_ETH, 2)
        
        FT_deposit = in_list[0]
        if FT_deposit == "None":
            FT_deposit_u = "None"
        else:
            FT_deposit_u = round(FT_deposit*price_ETH, 2)

        FT_withdraw = out_list[0]
        if FT_withdraw == "None":
            FT_withdraw_u = "None"
        else:
            FT_withdraw_u = round(FT_withdraw*price_ETH, 2)

        st.markdown(f'<a href="{FT_url}" target="_blank"><img src="{FT_image}" width="100%" height="100%"></a>', unsafe_allow_html=True)
        # st.image("https://forkast.news/wp-content/uploads/2023/08/Friend.tech-logo-1260x709.jpeg", use_column_width=True)
        # Display the 4 values
        st.markdown(f"**Price:** <span style='font-size: 18px; color: blue;'>{FT_price}</span> ETH (~{FT_price_u} USD)", unsafe_allow_html=True)
        st.markdown(f"**Total supply:** <span style='font-size: 18px; color: blue;'>{vals[1]}</span>", unsafe_allow_html=True)
        st.markdown(f"**All Deposit:** <span style='font-size: 18px; color: blue;'>{FT_deposit}</span> ETH (~{FT_deposit_u} USD)", unsafe_allow_html=True)
        st.markdown(f"**All Withdraw:** <span style='font-size: 18px; color: blue;'>{FT_withdraw}</span> ETH (~{FT_withdraw_u} USD)", unsafe_allow_html=True)
        FT_hours = st.slider("Check Buy/Sell in hours:", 0, 72, value=24, key = 1)
        update_data(data_list[0], "FT", FT_hours)

    with col3:
        NBC_image = "https://pbs.twimg.com/media/F8Kn5aeagAAWnpK.jpg:large"
        NBC_url = f"https://pro.newbitcoincity.com/alpha/profile/{wall_list[1]}"
        st.markdown(f'<a href="{NBC_url}" target="_blank"><img src="{NBC_image}" width="100%" height="100%"></a>', unsafe_allow_html=True)
        # st.image("https://pbs.twimg.com/media/F8Kn5aeagAAWnpK.jpg:large", use_column_width=True)
        NBC_price = vals[2]
        if NBC_price == "None":
            NBC_price_u = "None"
        else:
            NBC_price_u = round(vals[2]*price_BTC, 2)
        
        NBC_deposit = in_list[1]
        if NBC_deposit == "None":
            NBC_deposit_u = "None"
        else:
            NBC_deposit_u = round(in_list[1]*price_BTC, 2)

        NBC_withdraw = out_list[1]
        if NBC_withdraw == "None":
            NBC_withdraw_u = "None"
        else:
            NBC_withdraw_u = round(out_list[1]*price_ETH, 2)
        if vals[2]!="None":
            formatted_val = round(vals[2],7)
            # st.write("Price:", f":orange[{formatted_val}]", "BTC")
            st.markdown(f"**Price:** <span style='font-size: 18px; color: orange;'>{formatted_val}</span> BTC (~{round(formatted_val*price_BTC, 2)} USD)", unsafe_allow_html=True)
        else:
            st.markdown(f"**Price:** <span style='font-size: 18px; color: orange;'>{NBC_price}</span> BTC (~{NBC_price_u} USD)", unsafe_allow_html=True)
        st.markdown(f"**Total supply:** <span style='font-size: 18px; color: orange;'>{vals[3]}</span>", unsafe_allow_html=True)
        st.markdown(f"**All Deposit:** <span style='font-size: 18px; color: orange;'>{NBC_deposit}</span> BTC (~{NBC_deposit_u} USD)", unsafe_allow_html=True)
        st.markdown(f"**All Withdraw:** <span style='font-size: 18px; color: orange;'>{NBC_withdraw}</span> ETH (~{NBC_withdraw_u} USD)", unsafe_allow_html=True)            
        # st.write("Total supply:", f":orange[{vals[3]}]")
        # st.write("All Deposit:", f":orange[{in_list[1]}]", "BTC")
        NBC_hours = st.slider("Check Buy/Sell in hours:", 0, 72, value=24, key = 3)
        update_data(data_list[1], "NBC", NBC_hours)

    with col4:
        SA_image = "https://lwcdn.freebitco.in/wp-content/uploads/2023/10/Stars-Arena-img.png"
        SA_url = f"https://starsarena.com/{user_input}/"
        SA_price = vals[4]
        if SA_price == "None":
            SA_price_u = "None"
        else:
            SA_price_u = round(SA_price*price_AVAX, 2)
        
        SA_deposit = in_list[2]
        if SA_deposit == "None":
            SA_deposit_u = "None"
        else:
            SA_deposit_u = round(SA_deposit*price_AVAX, 2)

        SA_withdraw = out_list[2]
        if SA_withdraw == "None":
            SA_withdraw_u = "None"
        else:
            SA_withdraw_u = round(SA_withdraw*price_AVAX, 2)
        # col11, col21 = st.columns(2)
        # st.image(SA_image, use_column_width=True)
        st.markdown(f'<a href="{SA_url}" target="_blank"><img src="{SA_image}" width="100%" height="100%"></a>', unsafe_allow_html=True)
        # Display the 4 values
        st.markdown(f"**Price:** <span style='font-size: 18px; color: red;'>{SA_price}</span> AVAX (~{SA_price_u} USD)", unsafe_allow_html=True)
        st.markdown(f"**Total supply:** <span style='font-size: 18px; color: red;'>{vals[5]}</span>", unsafe_allow_html=True)
        st.markdown(f"**All Deposit:** <span style='font-size: 18px; color: red;'>{SA_deposit}</span> AVAX (~{SA_deposit_u} USD)", unsafe_allow_html=True)
        st.markdown(f"**All Withdraw:** <span style='font-size: 18px; color: red;'>{SA_withdraw}</span> AVAX (~{SA_withdraw_u} USD)", unsafe_allow_html=True)
        SA_hours = st.slider("Check Buy/Sell in hours:", 0, 72, value=24, key = 2)
        update_data(data_list[2], "SA", SA_hours)
        
        # st.write("Price:", f":orange[{vals[4]}]", "AVAX")
        # st.write("Total supply:", f":orange[{vals[5]}]")
        # st.write("All Deposit:", f":orange[{in_list[2]}]", "AVAX")

    with col5:
        TOMO_image = "https://pbs.twimg.com/media/F8PojQDbMAAKPdZ?format=jpg&name=medium"
        st.markdown(f'<a><img src="{TOMO_image}" width="100%" height="100%"></a>', unsafe_allow_html=True)
        st.markdown(f"**(TOMO is under-developing...)**", unsafe_allow_html=True)
        st.markdown(f"**Price:** <span style='font-size: 18px; color: orange;'>None</span> AVAX", unsafe_allow_html=True)
        st.markdown(f"**Total supply:** <span style='font-size: 18px; color: orange;'>None</span>", unsafe_allow_html=True)
        st.markdown(f"**All Deposit:** <span style='font-size: 18px; color: orange;'>None</span> AVAX", unsafe_allow_html=True)
        # st.write("(TOMO is under-developing...)")
        # st.image(TOMO_image, use_column_width=True)
        # if vals[2]!="None":
        #     formatted_val = "{:.5f}".format(vals[2])
        #     st.write("Price:", f":orange[None]", "ETH")
        # else:
        # st.write("Price:", f":orange[None]", "ETH")
        # st.write("Total supply:", f":orange[None]")


st.write("Produced by 0x0funky: ", "https://twitter.com/0x0funky ")
st.write("FT: ", "https://friend.tech/0x0funky")
st.write("SocialFi Tracker open for free now, will open for key holders only in the future.")
# if auto_update:
#     rerun_flag =True
#     time.sleep(10)  # wait for 10 seconds
#     st.rerun()