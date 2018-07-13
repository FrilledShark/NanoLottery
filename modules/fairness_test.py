from random import choice
from collections import Counter
from modules import fair

#
# Generates random hexs and runs the fair module on it. If the Bitcoin network is random,
# After about 2 minutes run, this was generated
# Counter({4: 45574, 6: 45502, 12: 45163, 10: 45153, 7: 45106, 1: 45093, 20: 45042, 17: 45028, 15: 44994, 19: 44991, 9: 44956, 11: 44917, 2: 44897, 13: 44891, 16: 44868, 8: 44835, 3: 44815, 18: 44793, 5: 44724, 14: 44659})
# Difference between highest and lowest is ~2%. The variance between
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