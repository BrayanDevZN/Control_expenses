"""
Junta a chave do jwt com a classe e os modulos
"""

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



    #Decide se vai buscar o usuario pelo token do cookie ou pelo email do body
    async def _get_user(self) -> None:

        self.cookie = self.req.cookies.get("user_token") 
        

        if self.cookie is None:

            data = await self.req.json()

            if not "email" in data.keys():

                raise TypeError("Expeted cookie or email")

            self.data = data["email"]
            self.search = "email"
            

        else:
            
            self.search = "public_id"
            

            self.data =  self.jwt.read(token=self.cookie)["public_id"]

    #Busca o usuario
    async def _user(self) -> None:

        self.user =  self.db.select(search=self.search, value=self.data)

    

    #Inicia a instancia do validador de /users
    async def _valid(self) -> None:

        instance = ValidUsers(request=self.req, security=Users(), user=self.user, token=self.cookie)
        self.result = await instance.run()

    #Executa os metodos e retorna o resultado da validação
    async def run(self) -> None|dict:

        await self._get_user()
        await self._user()
        await self._valid()
        


    
        return self.result

        


    