from src.logs.log import logger


"""
Cria as tabelas do banco se não existir
"""

from sqlalchemy import Engine, text
class TablesDbError(Exception):
    pass

class TablesDb:

    def __init__(self, engine: Engine)-> None:

        #engine do banco de dados
        self.eng = engine


    #comandos sql apara a criação de cada tabela
    def _sql(self) -> None:

        self.sql = {
            "users": """
                    create table if not exists users(
                    id serial primary key,
                    public_id uuid,
                    name text not null,
                    email text not null,
                    password text,
                    role text not null,
                    wage numeric(10, 2),
                    created_at timestamptz default current_timestamp
                    )
                    """,
            "expanses": """
                        create table if not exists expanses( 
                        id serial primary key,
                        user_id int,
                        name text not null unique,
                        quantity int not null,
                        price numeric (10,2),
                        created_at timestamptz default current_timestamp,
                        foreign key (user_id) references users(id) on delete cascade
                        )
                        """     
        }

    #Executa as querys
    def _query(self) -> None:

        try:

            with self.eng.begin() as session:

                for table, sql in self.sql.items():

                    logger.info(f"Criando {table} se não existir")


                    session.execute(text(sql))

        except Exception as e:

            logger.error(e)

            raise TablesDbError(e)


    #Executa os metodos
    def run(self) -> None:

        self._sql()
        self._query()

        

    

    
        