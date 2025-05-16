import random
import string

def generate_integer(lower = 0, upper = int(1e18)):
    return random.randint(lower, upper)

def generate_float(lower = 0, upper = 1e18, precision = 6):
    return round(random.uniform(lower, upper), precision)

def generate_char(charset = ['upper', 'lower', 'digit', 'special']):
    sets = {
        'upper': string.ascii_uppercase,      # A–Z
        'lower': string.ascii_lowercase,      # a–z
        'digit': string.digits,               # 0–9
        'special': string.punctuation         # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    }

    pool = ''.join(sets[key] for key in charset if key in sets)

    return random.choice(pool)

def generate_string(size, charset = ['upper', 'lower', 'digit', 'special']):
    sets = {
        'upper': string.ascii_uppercase,   # A–Z
        'lower': string.ascii_lowercase,   # a–z
        'digit': string.digits,            # 0–9
        'special': string.punctuation      # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    }

    pool = ''.join(sets[key] for key in charset if key in sets)

    return ''.join(random.choice(pool) for _ in range(size))