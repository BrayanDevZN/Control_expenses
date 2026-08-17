"""
Carrega as variaveis de ambiente
"""

class NotFoundUrlError(str):

    pass

try:

    #Se o arquivo .env existir, ele puxa do caminho, caso contrario, ele carrega da raiz
    import os

    if os.path.exists("infra/core/.env"):

        from pathlib import Path

        
        BASE_DIR = Path(__file__).resolve().parent / ".env"

        #Carrega as variaveis de ambiente

        from dotenv import load_dotenv

        load_dotenv(BASE_DIR)


    url = os.getenv("url")

    #Se a url não existir, levanta erro
    if url is None:

        raise NotFoundUrlError("Not found url")

except Exception as e:

    raise Exception(e)
        
        

        
        

    


        
        
        
        

        