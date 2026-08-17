from logs.log import logger

"""
Cria e le token jwt
"""

import jwt

class JwtTokenError(Exception):
    pass


class JwtToken:

    def __init__(self, sing:str)-> None:

        self.sing = sing
        self.alg = "HS256"
        

    #Cria o token
    def create(self, payload:dict) -> str:

        try:

            logger.info("Criando token...")

            token = jwt.encode(
                key=self.sing,
                payload=payload,
                algorithm=self.alg
            )

            return token

        except Exception as e:

            logger.error(e)
            raise JwtTokenError(e)


    #Le o token
    def read(self, token:str) -> dict:

        try:

            logger.info("Lendo token...")

            payload = jwt.decode(
                key=self.sing,
                algorithms=[self.alg],
                jwt=token
            )

            return payload

        except Exception as e:

            logger.error(e)
            raise JwtTokenError(e)



    