"""
Classe que serve pra pegar o public id do usuario e retornar o id 
"""

from fastapi import Request, HTTPException
from service.db import control_db
from infra.manage import engine
from service.encode import jwt



class GetUser:

    def __init__(self, request: Request)-> None:

        self.req = request
        
   

    #Pega o  public id do token
    def _public(self) -> None:
        token = self.req.cookies.get("user_token")

        self.public_id = jwt.read(token=token)

    #Faz a busca do usuario do banco de dados
    def _user(self) -> None:

        self.user = control_db.users.select(int(self.public_id))

    #Valida se o usuario existe ou não
    def _exists(self) -> None|HTTPException:

        return HTTPException(
            detail="user not found", status_code=401
        ) if self.user is None else None

    #Executa os metodos e retornar o id se o usaurio existir
    def run(self) -> int|None:

        self._public()
        self._user()

        exists = self._exists()

        return exists if exists else self.user["id"]




    
        