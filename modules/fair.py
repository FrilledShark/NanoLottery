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


# Getting the roll as a decimal number between 0 and 1. 1 is the highest possible roll and 0 is the lowest.
def roll(block_hash):
    length = 8
    max_hex = "".join("f" for x in range(length))
    max_int = int(max_hex, 16)
    roll_int = int(block_hash[-length:], 16)
    return roll_int/max_int


# Converting the decimal number to a range.
def roll_between(high, roll_deci):
    # This counts as round_down. Every number has the same potential for round down.
    # Eg. 20 has from 20 to 21 and 1 has from 1 to 2.
    between_roll = int(roll_deci * high) + 1
    return between_roll
