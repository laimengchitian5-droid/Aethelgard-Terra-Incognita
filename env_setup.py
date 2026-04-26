import os

def check_env():
    if not os.path.exists("data"):
        os.makedirs("data")
