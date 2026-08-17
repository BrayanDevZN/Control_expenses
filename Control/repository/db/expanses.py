from logs.log import logger
import uuid
"""
mexe na tabela expanses
"""

class ExpansesDbError(Exception):
    pass



from sqlalchemy import text, Engine
from typing import Literal

class ExpansesDb:

    def __init__(self, eng:Engine)-> None:

        self.eng = eng


    #Insere no banco
    def insert(self, user_id:int, name:str, quantity:int, price:float) -> dict:

        try:

            logger.info(f"Criando gasto {name}...")

            with self.eng.begin() as session:

                result =session.execute(
                    text("insert into expanses(user_id, name, quantity, price) values(:public_id, :name, :quantity, :price) returning *"),
                    {"user_id": user_id, "name":name, "quantity":quantity, "price":price}
                )

            return result.mappings().fetchone()


        except Exception as e:
            logger.error(e)
            raise ExpansesDbError(e)

        
    #Busca gasto(s)
    def select(self, user_id:int = None) -> dict|None:

        try:

            logger.info("Buscando gasto...")

            sql = "select * from expanses" if user_id is None else "select * from expanses where user_id = :user_id"

            with self.eng.begin() as session:

                result = session.execute(
                    text(sql), {"user_id": user_id}
                )

            return result.mappings().fetchone()

        except Exception as e:
            logger.error(e)
            raise ExpansesDbError(e)


    #Atualiza algo do gasto
    def update(self, user_id:int, set:Literal["name", "quantity", "price"], value:str|float|int) -> None:

        try:

            logger.info(f"Atualizando {set} para {value}...")

            with self.eng.begin() as session:

                session.execute(
                    text("update users set :set = :value where user_id = :user_id"),
                    {"set":set, "value":value, "user_id": user_id}
                
                )


        except Exception as e:
            logger.error(e)
            raise ExpansesDbError(e)

    #Deleta gsto
    def delete(self, user_id:int=None) -> None:
    
            try:
    
                logger.info(f"deletando {"gastos" if user_id is None else "gasto"}...")
    
                with self.eng.begin() as session:
    
                    session.execute(
                        text("delete from expanses where public_id = :public_id" if user_id is not None else "delete from expanses"),
                        {"user_id":user_id}
                    )
    
    
            except Exception as e:
                logger.error(e)
                raise ExpansesDbError(e)
    

        
        
