import os
import boto3 
import client

idp_client = boto3.client(
    'cognito-idp',
    region_name = "ap-northeast-1",
)

def main():
    c = client.Client(
        client=idp_client,
        user_pool_id=os.getenv("COUSER_POOL_ID"),
        client_id=os.getenv("APP_CLIENT_ID"),
    )

    c.signin(
        username=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD")
    )
    
if __name__ == '__main__':
    main()