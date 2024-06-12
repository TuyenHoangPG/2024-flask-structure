import random
import string


def get_random_string(length=16):
    letters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(letters) for i in range(length))
