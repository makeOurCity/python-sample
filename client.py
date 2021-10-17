
from warrant.aws_srp import AWSSRP

class Client:
    client = None
    user_pool_id = None
    client_id = None
    auth = None

    __id_token = None
    __refresh_token = None
    __access_token = None


    def __init__(self, client, user_pool_id: str, client_id: str):
        self.client = client
        self.user_pool_id = user_pool_id
        self.client_id = client_id
    
    @property
    def id_token(self):
        return self.__id_token

    def signin(self, username: str, password: str):
        aws = AWSSRP( # docs: https://github.com/capless/warrant
            username=username,
            password=password,
            pool_id=self.user_pool_id,
            client_id=self.client_id, 
            client=self.client,
        )

        tokens = aws.authenticate_user()

        result = tokens.get("AuthenticationResult", None)
        if result is not None:
            self.__id_token = result.get("IdToken", None)
            self.__refresh_token = result.get("RefreshToken", None)
            self.__access_token = result.get("AccessToken", None)

        return tokens