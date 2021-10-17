import os
from os import path
import json

import boto3 
import requests
from dotenv import load_dotenv

import client


dotenv_path = path.join(path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

idp_client = boto3.client(
    'cognito-idp',
    region_name = "ap-northeast-1",
)

def main():
    c = client.Client(
        client=idp_client,
        base_url=os.getenv("ORION_ENDPOINT"),
        user_pool_id=os.getenv("USER_POOL_ID"),
        client_id=os.getenv("APP_CLIENT_ID"),
    )

    c.signin(
        username=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD")
    )

    # print(f"idToken: {c.id_token}")

    resp = c.do(requests.Request('GET', "/version"))
    j = json.loads(resp.content)
    print(json.dumps(j, indent=2))
    
    
if __name__ == '__main__':
    main()