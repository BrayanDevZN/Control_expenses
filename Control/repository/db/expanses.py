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
                    text("insert into expanses(user_id, name, quantity, price) values(:user_id, :name, :quantity, :price) returning *"),
                    {"user_id":user_id, "name":name, "quantity":quantity, "price":price}
                )

            return result.mappings().fetchone()


        except Exception as e:
            logger.error(e)
            raise ExpansesDbError(e)

        
    #Busca gasto(s)
    def select(self, user_id:int, name:str=None) -> dict|None:

        try:

            logger.info(f"Buscando {"gastos" if name is None else name}...")

            

            sql = "select name, quantity, price, (quantity * price) as total from expanses where user_id = :user_id" if name is None else "select name, quantity, price, (quantity * price) as total from expanses where user_id = :user_id and name = :name"

           
            with self.eng.begin() as session:

                result = session.execute(
                    text(sql), {"user_id": user_id} if name is None else {"user_id": user_id, "name":name}
                )

            return result.mappings().fetchone() if name is not None else result.mappings().fetchall()

        except Exception as e:
            logger.error(e)
            raise ExpansesDbError(e)


    #Atualiza algo do gasto
    def update(self, user_id:int,name:str, set:Literal["name", "quantity", "price"], value:str|float|int) -> None:

        try:

            logger.info(f"Atualizando {set} para {value}...")

            with self.eng.begin() as session:

                session.execute(
                    text(f"update users set {name} = :value where user_id = :user_id and name = :name"),
                    {"value":value, "user_id": user_id}
                
                )


        except Exception as e:
            logger.error(e)
            raise ExpansesDbError(e)

    #Deleta gasto
    def delete(self, user_id:int=None, name:str=None) -> None:
    
            try:
    
                logger.info(f"deletando {"gastos" if name is None else name}...")

                if user_id is None:
                    sql = "delete from expanses"
                    params = None

                elif user_id is not None and name is None:
                    sql = "delete from expanses where user_id = :user_id"
                    params = {"user_id": user_id}

                else:
                    sql = "delete from expanses where user_id = :user_id and name = :name"
                    params = {"user_id": user_id, "name":name}


    
                with self.eng.begin() as session:

                    if params is None:
    
                        session.execute(
                            text(sql)
                        )

                    else:
                        session.execute(
                                        text(sql), params
                                        )
        
    
            except Exception as e:
                logger.error(e)
                raise ExpansesDbError(e)
    

        
        
