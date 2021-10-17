import os
from os import path

import boto3 
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
        user_pool_id=os.getenv("USER_POOL_ID"),
        client_id=os.getenv("APP_CLIENT_ID"),
    )

    tokens = c.signin(
        username=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD")
    )

    print(tokens)
    
if __name__ == '__main__':
    main()