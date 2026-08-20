"""
Regra de negocio de users
"""
from fastapi import Request
from src.domain.encode.hash import HashPass
import json
class ValidUsers:

    def __init__(self,security, request:Request, user: str|None, token:str|None)-> None:

        self.req = request
        self.user = user
        self.sec = security
        self.token = token

    #Confere se o usaurio existe
    async def _exists(self) -> dict:

        if self.req.method in self.sec.exists["methods"] and self.req.url.path == self.sec.exists["path"] and not self.req.url.path in self.sec.exists["ignore"]:

            return  {"error": f"{self.user["name"]} not exists", "status_code": 401} if self.user is None else  {"error": None, "status_code": 201}

        return  {"error": None, "status_code": 201}

    #Confere se a senha inserida e igual do banco
    async def _check(self) -> dict:

        if self.req.method in self.sec.check["methods"] and self.req.url.path == self.sec.check["path"] and not self.req.url.path in self.sec.exists["ignore"]:



            body = await self.req.body()
            data = json.loads(body.decode("utf-8"))

            hash = HashPass()

            
            return ({"error": "invalid pass", "status_code": 501} 
                    if not hash.valid(password_hash=self.user["password"], password=data["password"]) and "password" in data
                    else {"error": None, "status_code": 201})

        return   {"error": None, "status_code": 201}

    #confere se o usuario não existe
    async def _not_exists(self) -> dict:

        if self.req.method in self.sec.not_exists["methods"] and self.req.url.path == self.sec.not_exists["path"] and not self.req.url.path in self.sec.not_exists["ignore"]:

            

            return   {"error": f"{self.user["name"]} exists", "status_code": 422} if self.user is not None else  {"error": None, "status_code": 201}

        return    {"error": None, "status_code": 201}

    #Adiciona o token
    async def _token(self) -> None:

        if self.req.method in self.sec.token["methods"] and self.req.url.path == self.sec.token["path"] and not self.req.url.path in self.sec.token["ignore"]:

            if self.token:
                new_headers = self.req.headers.mutablecopy()
                new_headers["X-user_token"] = str(self.token)
                self.req._headers = new_headers
                self.req.scope["headers"] = new_headers.raw

            self.result["token"] = self.token



    #Executa os metodos de verificação
    async def _methods(self) -> None:

        execute = [self._not_exists, self._exists, self._check]

        for method in execute:

            result = await method()

            if result["error"] is not None:
                break

        self.result = result

    #Executa o metodo _methods e _token e retorna a self.result
    async def run(self) -> dict:

        await self._methods()
        await self._token()

        return self.result

        

        
        
        

    
    

        


    



    
        

