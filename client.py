
from warrant.aws_srp import AWSSRP

class Client:
    client = None
    user_pool_id = None
    client_id = None
    auth = None

    def __init__(self, client, user_pool_id: str, client_id: str):
        self.client = client
        self.user_pool_id = user_pool_id
        self.client_id = client_id

    def signin(self, username: str, password: str):
        aws = AWSSRP(
            username=username,
            password=password,
            pool_id=self.user_pool_id,
            client_id=self.client_id, 
            client=self.client,
        )

        tokens = aws.authenticate_user()    

        return tokens