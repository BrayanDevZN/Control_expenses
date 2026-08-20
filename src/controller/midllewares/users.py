"""
Cria a classe do midlleware
"""

from src.service.manage import ValidMidlleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse


class Midlleware(BaseHTTPMiddleware):

    async def dispatch(self, request:Request, call_next):

        instance = ValidMidlleware(request=request)
        midlleware = await instance.run()

       
        if midlleware["error"] != None:
        

            return JSONResponse(
                content=midlleware["error"], status_code=midlleware["status_code"]
            )


        response =  await call_next(request)


        if "token" in midlleware.keys():
        
            response.set_cookie(
                key="user_token",
                value=midlleware["token"],
                samesite="strict",
                httponly=True
            )

       
        return response
        
        

        
