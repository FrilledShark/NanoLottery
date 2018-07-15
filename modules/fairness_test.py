from random import choice
from collections import Counter
from modules import fair

#
# Generates random hexs and runs the fair module on it. If the Bitcoin network is random,
# After about 2 minutes run, this was generated
# Counter({18: 200538, 16: 200410, 9: 200404, 13: 200244, 14: 200240, 10: 200189, 20: 200161, 11: 200057, 19: 200022, 8: 200022, 7: 200021, 12: 200019, 1: 199996, 15: 199948, 6: 199893, 3: 199872, 4: 199762, 2: 199655, 17: 199290, 5: 199258})
# Difference between highest and lowest is ~0.63%.
#

hexadecimal = '0123456789abcdef'

# Generates random hex
def random_hexa():
    return "".join(choice(hexadecimal) for _ in range(8))


if __name__ == "__main__":
    rolls = []
    while True:
        rolls.append(fair.roll_between(20, fair.roll(random_hexa())))
        if len(rolls) % 100000 == 1:
            print(Counter(rolls))
