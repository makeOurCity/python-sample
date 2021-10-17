import urllib
from warrant.aws_srp import AWSSRP
from requests import Request, Session, Response

class Client:
    client = None
    user_pool_id = None
    client_id = None

    __id_token = None
    __refresh_token = None
    __access_token = None

    __base_url = None
    __session = None
    __timeout = None


    def __init__(
        self,
        client,
        base_url: str,
        user_pool_id: str,
        client_id: str,
        * ,
        session = None,
        timeout = 5,
    ):
        self.client = client
        self.user_pool_id = user_pool_id
        self.client_id = client_id
        self.__session = session or Session()
        self.__base_url = base_url
        self.__timeout = timeout
    
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
    
    def do(self, req: Request) -> Response:
        req.headers['Authorization'] = self.__id_token
        print('do')
        req.url = urllib.parse.urljoin(self.__base_url, req.url)

        print(req.headers)
        print(req.url)
        return self.__session.send(req.prepare(), timeout=self.__timeout)