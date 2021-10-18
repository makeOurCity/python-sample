import os
from os import path
import json

import boto3 
import requests
from dotenv import load_dotenv

import client


dotenv_path = path.join(path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

def main():
    c = client.Client(
        session=boto3.Session(region_name="ap-northeast-1"),
        base_url=os.getenv("ORION_ENDPOINT"),
        user_pool_id=os.getenv("USER_POOL_ID"),
        client_id=os.getenv("APP_CLIENT_ID"),
    )

    c.signin(
        username=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD")
    )

    print(f"idToken: {c.id_token}")

    resp = c.do(requests.Request('GET', "/version"))
    j = json.loads(resp.content)
    print(json.dumps(j, indent=2))

    print("expired:", c.is_token_expired())
    
    
if __name__ == '__main__':
    main()