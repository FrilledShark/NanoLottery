import requests


def blockchain_api(height):
    while True:
        try:
            resp = requests.get(f'https://blockchain.info/block-height/{height}?format=json')
            block = resp.json()
            block_hash = block["blocks"][0]['hash']
            break
        except:
            print("Cannot get height. Trying again.")
    return block_hash


def last_blockchain():
    while True:
        try:
            resp = requests.get('https://blockchain.info/q/getblockcount')
            block = resp.json()
            break
        except:
            print("Cannot get last height. Trying again.")
    return block


def roll(block_hash):
    length = 8
    max_hex = "".join("f" for x in range(length))
    max_deci = int(max_hex, 16)
    roll_hash = int(block_hash[-length:], 16)
    return roll_hash/max_deci


def roll_between(high, roll_int):
    between_roll = round(roll_int * high) + 1
    # Highest and lowest share their win rate. Add them together to get correct roll.
    # Also fixes the problem that this generates high + 1 results.
    if between_roll == high + 1:
        return 1
    return between_roll
