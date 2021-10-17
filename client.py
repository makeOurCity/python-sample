

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
        res = self.client.admin_initiate_auth(
            UserPoolId = self.user_pool_id,
            ClientId = self.client_id,
            AuthFlow = "ADMIN_NO_SRP_AUTH",
            AuthParameters = {
                "USERNAME": username,
                "PASSWORD": password,
            }
        )

        return res