"""
Regra de negocio de users
"""
from fastapi import Request, HTTPException
from domain.encode.hash import HashPass

class ValidUsers:

    def __init__(self,security, request:Request, user: str|None)-> None:

        self.req = request
        self.user = user
        self.sec = security

    #Confere se o usaurio existe
    async def _exists(self) -> None|HTTPException:

        if self.req.method in self.sec.exists["methods"] and self.req.url.path == self.sec.exists["path"] and not self.req.url.path in self.sec.exists["ignore"]:

            return await HTTPException(
                detail="user not found",
                status_code=401
            ) if self.user is None else None

        return None

    #Confere se a senha inserida e igual do banco
    async def _check(self) -> None|HTTPException:

        if self.req.method in self.sec.check["methods"] and self.req.url.path == self.sec.check["path"] and not self.req.url.path in self.sec.exists["ignore"]:



            body = await self.req.json()
            hash = HashPass()

            
            return await HTTPException(
                status_code=501, detail="Invalid pass"
            ) if not hash.valid(password_hash=self.user["password"], password=body["password"]) and "password" in body else None

        return None

    #confere se o usuario não existe
    async def _not_exists(self) -> None|HTTPException:

        if self.req.method in self.sec.not_exists["methods"] and self.req.url.path == self.sec.not_exists["path"] and not self.req.url.path in self.sec.not_exists["ignore"]:

            return await  HTTPException(
                detail="exits user",
                status_code=501
            ) if self.user is not None else None

        return None




    #Executa os metodos e retorna None se nenhum metodo for executadp
    async def run(self) -> None|HTTPException:

        execute = [self._not_exists, self._exists, self._check]

        for method in execute:

            result = await method()

            if result is not None:
                return await result

        return await None

        

    
    

        


    



    
        

