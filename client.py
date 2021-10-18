import urllib
import boto3
from warrant.aws_srp import AWSSRP
from warrant import Cognito
from requests import Request, Session, Response

class Client:
    client = None
    user_pool_id = None
    client_id = None

    __region_name = None

    __id_token = None
    __refresh_token = None
    __access_token = None

    __base_url = None
    __requests_session = None
    __timeout = None


    def __init__(
        self,
        session: boto3.Session,
        base_url: str,
        user_pool_id: str,
        client_id: str,
        * ,
        timeout: int = 5,
        requests_session: Session = None,
    ):
        self.client = session.client('cognito-idp')
        self.__region_name = session.region_name
        self.__requests_session = requests_session or Session()
        self.user_pool_id = user_pool_id
        self.client_id = client_id
        self.__base_url = base_url
        self.__timeout = timeout
        
    
    @property
    def id_token(self):
        return self.__id_token

    def signin(self, username: str, password: str):
        aws = AWSSRP( # https://github.com/capless/warrant#using-awssrp
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

    @property
    def __cognito(self) -> Cognito:
        return Cognito( 
            self.user_pool_id,
            self.client_id,
            id_token=self.__id_token,
            refresh_token=self.__refresh_token,
            access_token=self.__access_token,
            user_pool_region=self.__region_name,
        )
    
    def is_token_expired(self):
        return self.__cognito.check_token() # https://github.com/capless/warrant#check-token 
    
    def do(self, req: Request) -> Response:
        req.headers['Authorization'] = self.__id_token
        req.url = urllib.parse.urljoin(self.__base_url, req.url)
        return self.__requests_session.send(req.prepare(), timeout=self.__timeout)