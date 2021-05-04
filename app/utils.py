import string
import random

def random_code():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))