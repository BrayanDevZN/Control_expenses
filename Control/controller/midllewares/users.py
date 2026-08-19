"""
Cria a classe do midlleware
"""

from service.manage import ValidMidlleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


class Midlleware(BaseHTTPMiddleware):

    async def dispatch(self, request:Request, call_next):

        instance = ValidMidlleware(request=request)
        midlleware = instance.run()

        if midlleware != None:

            return midlleware

        return await call_next(request)


        
