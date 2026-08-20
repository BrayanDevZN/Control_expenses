"""
junta os modulos
"""

from src.repository.db.users import UsersDb
from src.repository.db.expanses import ExpansesDb
from sqlalchemy import Engine
class ControlDb:

    def __init__(self, engine: Engine)-> None:

        self.users = UsersDb(eng=engine)
        self.expanses = ExpansesDb(eng=engine)


        
        