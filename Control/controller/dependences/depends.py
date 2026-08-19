"""
Função que vai servir de dependencia
"""

from service.manage import GetUser
from fastapi import Request,HTTPException

def depends(request:Request) -> int|HTTPException:

    try:

        instance = GetUser(request=request)

        return instance.run()

    except Exception as e:

        raise Exception(e)