from dotenv import load_dotenv
import os

from google.cloud import storage
from google.oauth2 import service_account

load_dotenv()

path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

print("PATH:", path)  # debug

credentials = service_account.Credentials.from_service_account_file(path)

client = storage.Client(credentials=credentials)

print("Conectado com sucesso")