"""
Junta a chave do jwt com a classe e os modulos
"""
import json
from src.domain.encode.jwt import JwtToken
from src.infra.manage import Users
from fastapi import Request
from src.infra.manage import sing, engine
from src.repository.manage import ControlDb
from src.domain.role.users import ValidUsers
#classe que junta as chave de seguranção com a validação de /users

class ValidMidlleware:

    def __init__(self, request:Request)-> None:

        self.req = request
        self.jwt = JwtToken(sing=sing)
        self.db = ControlDb(engine=engine).users
        self.cookie = self.req.cookies.get("user_token")
        self.instance = ValidUsers(request=self.req, security=Users(),  token=self.cookie)



    #Decide se vai buscar o usuario pelo token do cookie ou pelo email do body
    async def _get_user(self) -> None:

        body = await self.req.body()
        self.body = json.loads(body.decode("utf-8")) if body else {}
        self.search = "email" if "email" in self.body else "public_id"
                            

    #confere se o token ja foi expirado
    async def _expired(self) -> None:

        if self.cookie is not None:

            expired = self.data["expired"]
            self.expired = self.instance.expired(expired=expired)

    #Pega o dado de busca
    async def _data(self) -> None:

        if self.search == "email":
    
                    if not "email" in self.body.keys():
                    
                        raise TypeError("Expeted cookie or email")
        
                    self.data = self.body["email"]
        
        else:
        
                    self.data = self.jwt.read(token=self.cookie)["public_id"]
                    
                        
    #Busca o usuario
    async def _user(self) -> None:

         
        self.user =  self.db.select(search=self.search, value=self.data)
        self.instance.user = self.user

    
    #Inicia a instancia do validador de /users
    async def _valid(self) -> None:

        self.result = await self.instance.run()

    #Executa os metodos e retorna o resultado da validação
    async def run(self) -> None|dict:

        await self._get_user()
        await self._data()
        await self._expired()

        if self.expired["error"] is not None:
             return self.expired

        await self._user()
        await self._valid()

        return self.result

        


    