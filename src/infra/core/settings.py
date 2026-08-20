from logs.log import logger

"""
Carrega as variaveis de ambiente
"""

class NotFoundUrlError(Exception):

    pass



class NotFoundSingError(Exception):
    pass

class NotFoundDomainError(Exception):
    pass


try:

    #Se o arquivo .env existir, ele puxa do caminho, caso contrario, ele carrega da raiz
    import os

    if os.path.exists("infra/core/.env") or os.path.exists("Control/infra/core/.env"):

        from pathlib import Path

        
        BASE_DIR = Path(__file__).resolve().parent / ".env"

        #Carrega as variaveis de ambiente

        from dotenv import load_dotenv

        load_dotenv(BASE_DIR)


    url = os.getenv("url")
    sing = os.getenv("sing")
    domain = os.getenv("domain")

    #Se a url não existir, levanta erro
    if url is None:
        logger.error("Not found url")

        raise NotFoundUrlError("Not found url")

    if sing is None:
        logger.error("Not found sing jwt")

        raise NotFoundSingError("Not found sing jwt")

    if domain is None:

        logger.error("Not found domain")

        raise NotFoundDomainError("Not found domain")

    

except Exception as e:
    logger.error(e)

    raise Exception(e)
        
        

        
        

    


        
        
        
        

        