"""
Inicia toda aplicação
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller.handles.users import router_users
from controller.midllewares.midlleware import Midlleware

class Main:

    def __init__(self)-> None:

        #Intancia do fast api
        self.app = FastAPI()

        #Intancias de cada prefixo de rota
        self.routes = [router_users]

    #adciona o midlleware
    def _midlleware(self) -> None:

        self.app.add_middleware(Midlleware)

    #Adicona as rotas
    def _router(self) -> None:

        for router in self.routes:

            self.app.include_router(router)

    #Configuração de cors
    def _cors(self) -> None:

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
            allow_credentials=True,
            expose_headers=[]
        )


    #Chama todos os metodos
    def run(self) -> FastAPI:

        self._midlleware()
        self._cors()
        self._router()
        return self.app


#Inicializa a instancia
if __name__ == "__main__":

    instance = Main()
    app = instance.run()




    
        