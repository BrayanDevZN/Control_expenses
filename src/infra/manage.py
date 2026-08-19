"""
junta os modulos
"""

#Pega a engine do banco
from infra.core.settings import url, sing, domain
from infra.database.connection import connection
from infra.core.security import Users
engine = connection(url)






#Cria as tabelas

if __name__ == "__main__":

    import sys

    if sys.argv[1] == "start_schema":
    

        from infra.database.tables import TablesDb

        tables = TablesDb(engine=engine)

        tables.run()

    else:

        raise Exception(f"Not expeted argument {sys.argv[0]}")

