import json
from azure.identity._credentials.chained import ChainedTokenCredential

import requests
import msal
from azure.identity import AzureCliCredential, ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

jsondata = open("config.json","r")
config = json.load(jsondata)

credential = ChainedTokenCredential(AzureCliCredential(),ManagedIdentityCredential())
secret_client = SecretClient(config["vault_url"], credential=credential)
aad_client_secret = secret_client.get_secret("AadClientSecret")

app = msal.ConfidentialClientApplication(
    client_id=config["client_id"],
    client_credential=aad_client_secret.value,
    authority=config["authority"],
)

result = None

result = app.acquire_token_silent(config["scope"], account=None)

if not result:
    result = app.acquire_token_for_client(scopes=config["scope"])

if "error" in result:
   print(result["error_description"])

if "access_token" in result:
    session = requests.sessions.Session()
    session.headers.update({'Authorization': f'Bearer {result["access_token"]}'})
    response = session.get("http://localhost:8080/weatherforecast?city=London")
    if response.status_code == 200 :
        print(response.content)
    else:
        print(f'Request failed. Response code: {response.status_code}, reason: {response.reason}')
