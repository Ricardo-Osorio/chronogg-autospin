import requests
import os

SPIN_URL = 'https://api.chrono.gg/quest/spin'
COINS_URL = 'https://api.chrono.gg/account/coins'


def spinCoin(jwt):
    response = requests.get(
        SPIN_URL,
        headers={
            'Authorization': jwt,
        },
    )

    if response.status_code == 200:
        resp = response.json()
        if resp is not None and resp != "":
            print('response json: ', resp)
        gain = resp['quest']['value']+resp['quest']['bonus']
        # haven't seen the response from the request when it's a chest spin
        # gain_chest = resp['chest']
        print('spun coin for a total of {} points'.format(gain))
        getCoins(jwt)
    elif response.status_code == 420:
        print('spin is still in cooldown')
    elif response.status_code == 404:
        print('token invalid')
    else:
        print('unhandled status code returned. Please check logs')


def getCoins(jwt):
    response = requests.get(
        COINS_URL,
        headers={
            'Authorization': jwt,
        },
    )

    if response.status_code == 200:
        balance = response.json()['balance']
        print(f'current balance: {balance}')
    elif response.status_code == 404:
        print('token invalid')
    else:
        print(f'Unhandled status code returned. Raw response: {response}')


def importEnvVars():
    jwt = os.getenv('JWT_TOKEN')
    if jwt is None or jwt == "":
        raise Exception('Environment variable JWT_TOKEN missing')
    return jwt


def lambda_handler(event, context):
    jwt = importEnvVars()
    print(f'Lambda started. Environment variable JWT_TOKEN: {jwt}')
    spinCoin(jwt)
