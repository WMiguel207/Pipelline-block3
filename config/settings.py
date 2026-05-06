from dotenv import load_dotenv
import os

load_dotenv()  # PRIMEIRO

print("Show env vars:" + str(os.environ))  # DEPOIS