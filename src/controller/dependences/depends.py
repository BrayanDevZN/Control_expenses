from src.logs.log import logger


"""
Função que vai servir de dependencia
"""

from src.service.manage import GetUser
from fastapi import Request,HTTPException

def depends(request:Request) -> int|HTTPException:

    try:

        instance = GetUser(request=request)

        return instance.run()

    except Exception as e:

        logger.error(e)

        raise Exception(e)