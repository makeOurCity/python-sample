import json
import os

import requests
from dotenv import load_dotenv
from pycognito.utils import RequestsSrpAuth
from requests.auth import AuthBase

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)


def get_auth() -> AuthBase:
    auth = RequestsSrpAuth(
        username=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD"),
        user_pool_id=os.getenv("USER_POOL_ID"),
        client_id=os.getenv("APP_CLIENT_ID"),
        user_pool_region=os.getenv("USER_POOL_REGION"),
    )
    return auth


def main():
    orion_endpoint = os.getenv("ORION_ENDPOINT")
    auth = get_auth()
    response = requests.get(orion_endpoint + "/version", auth=auth)
    print(f"TOKEN: {auth.cognito_client.access_token}")
    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    main()
