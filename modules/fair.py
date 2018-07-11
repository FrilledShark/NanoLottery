import requests
from random import choice
from collections import Counter

def blockchain_api(height):
    resp = requests.get(f'https://blockchain.info/block-height/{height}?format=json')
    block = resp.json()
    hash = block["blocks"][0]['hash']
    return hash


def last_blockchain():
    resp = requests.get('https://blockchain.info/q/getblockcount')
    block = resp.json()
    return block

def roll(block_hash):
    length = 8
    max_hex = "".join("f" for x in range(length))
    max_deci = int(max_hex, 16)
    roll_hash = int(block_hash[-length:], 16)
    return roll_hash/max_deci


def roll_between(high, roll):
    between_roll = round(roll * high) + 1
    # Highest and lowest share their win rate. Add them together to get correct roll.
    # Also fixes the problem that this generates high + 1 results.
    if between_roll == high + 1:
        return 1
    return between_roll


if __name__ == "__main__":
    rolls = []
    while True:
        hex_list = "0123456789ABCDEF"
        hex_roll = "".join(choice(hex_list) for x in range(8))
        float_roll = roll(hex_roll)
        rolls.append(roll_between(10, float_roll))

        if len(rolls) % 1000 == 0:
            print(Counter(rolls))