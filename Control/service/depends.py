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
    async def _exists_user(self) -> None|HTTPException:

        return await  HTTPException(
            detail="user not found", status_code=401
        ) if self.user is None else None


    #Confere se o produto não existe, ele vai ser executado somente na rota de criação de gastos
    async def _not_exists(self) -> None|HTTPException:

        if self.req.method == "POST":

            body =  await self.req.json()

            expanse = control_db.expanses.select(user_id=self.user["id"], name=body["name"])

            return await  HTTPException(
                detail=f"{body["name"]} exists"
            ) if expanse is not None else None

    #Se a validação de gasto o usuario não for None, ele retorna o erro
    async def _valid(self) -> None|HTTPException:

        user= await self._exists_user()
        expanse = await self._not_exists()

        if user is not None:

            return user

        elif expanse is not None:
            return expanse

        return None

    
    #Executa os metodos e retornar o id se o usaurio existir
    async def run(self) -> int|None:

        self._public()
        self._user()

        exists = await self._valid()

        return await exists if exists else self.user["id"]




    
        