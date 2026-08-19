from logs.log import logger
import uuid
"""
mexe na tabela users
"""

class UsersDbError(Exception):
    pass



from sqlalchemy import text, Engine
from typing import Literal

class UsersDb:

    def __init__(self, eng:Engine)-> None:

        self.eng = eng


    #Insere no banco
    def insert(self, name:str, email:str, password:str, role:Literal["admin", "dev", "user"]) -> dict:

        try:

            logger.info(f"Criando usuario {name}...")

            with self.eng.begin() as session:

                result =session.execute(
                    text("insert into users(public_id, name, email, password, role) values(:public_id,:name, :email, :password, :role) returning public_id, name, id"),
                    {"public_id": uuid.uuid4(), "name": name, "email": email, "password": password, "role":role}
                )

            return result.mappings().fetchone()


        except Exception as e:
            logger.error(e)
            raise UsersDbError(e)

    #Busca usuario pelo id publico ou email
    def select(self, search:int|str) -> dict|None:

        try:

            logger.info("Buscando usuario...")

            data = "email" if isinstance(search, str) else "public_id"

            with self.eng.begin() as session:

                result = session.execute(
                    text("select * from users where :data = :search"), {"data":data, "search":search}
                )

            return result.mappings().fetchone()

        except Exception as e:
            logger.error(e)
            raise UsersDbError(e)


    #Atualiza a senha
    def update(self, public_id:int, new_pass:str) -> None:

        try:

            logger.info("Atualizando senha...")

            with self.eng.begin() as session:

                session.execute(
                    text("update users set password = :new_pass where public_id = :public_id"),
                    {"public_id": public_id, "new_pass": new_pass}
                )


        except Exception as e:
            logger.error(e)
            raise UsersDbError(e)

    #Deleta usuario
    def delete(self, public_id:int) -> None:
    
            try:
    
                logger.info("deletando usuario...")
    
                with self.eng.begin() as session:
    
                    session.execute(
                        text("delete from users where public_id = :public_id"),
                        {"public_id": public_id}
                    )
    
    
            except Exception as e:
                logger.error(e)
                raise UsersDbError(e)
    

        
        


        


