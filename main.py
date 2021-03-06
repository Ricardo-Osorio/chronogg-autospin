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
        gain = resp['quest']['value']+resp['quest']['bonus']
        chest_gain = resp['chest']['base']+resp['chest']['bonus'] if len(resp['chest']) else 0
        msg = 'spun coin for a total of {} points'.format(gain)
        if chest_gain > 0:
            msg += ' plus {} from a chest'.format(chest_gain)
        print(msg)
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
