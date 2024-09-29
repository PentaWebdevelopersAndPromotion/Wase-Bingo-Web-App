import random

def newID(prefix: str, length=8):
    alphanumerics = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return prefix + ''.join(random.choice(alphanumerics) for _ in range(length))
