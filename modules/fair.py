import requests

def blockchain_api(height):
    resp = requests.get(f'https://blockchain.info/block-height/{height}?format=json')
    block = resp.json()
    hash = block["blocks"][0]['hash']
    return hash


def roll(hash):
    length = 16
    max_hex = "".join("f" for x in range(length))
    print(max_hex)
    max_deci = int(max_hex, 16)
    roll_hash = int(hash[-length:], 16)
    return roll_hash/max_deci

def roll_between(high, roll):
    return round(roll*high)+1


if __name__ == "__main__":
    hash = blockchain_api(100005)
    print(hash[-16:])
    rol = roll(hash)
    print(rol)
    roll_cal = roll_between(1000, rol)
    print(roll_cal)