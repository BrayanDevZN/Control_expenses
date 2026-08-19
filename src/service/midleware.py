"""
Junta a chave do jwt com a classe e os modulos
"""

from domain.encode.jwt import JwtToken
from infra.manage import Users
from fastapi import Request
from infra.manage import sing, engine
from repository.manage import ControlDb
from domain.role.users import ValidUsers, HTTPException
#classe que junta as chave de seguranção com a validação de /users

class ValidMidlleware:

    def __init__(self, request:Request)-> None:

        self.req = request
        self.jwt = JwtToken(sing=sing)
        self.db = ControlDb(engine=engine).users



    #Decide se vai buscar o usuario pelo token do cookie ou pelo email do body
    async def _get_user(self) -> None:

        cookie = self.req.cookies.get("user_token")

        if cookie is None:

            data = await dict(self.req.json())

            if not "email" in data.keys():

                raise TypeError("Expeted cookie or email")

            self.data = data["email"]

        else:

            self.data = self.jwt.read(token=cookie["user_token"])

    #Busca o usuario
    async def _user(self) -> None:

        self.user = await self.db.select(search=self.data)

    #Inicia a instancia do validador de /users
    async def _valid(self) -> None:

        instance = ValidUsers(request=self.req, security=Users(), user=self.user)
        self.result = await instance.run()

    #Executa os metodos e retorna o resultado da validação
    def run(self) -> None|HTTPException:

        self._get_user()
        self._user()
        return self._valid()

        


    