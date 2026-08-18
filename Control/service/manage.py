"""
junta a classe do banco com a engine
"""


from infra.manage import engine, sing
from repository.manage import ControlDb

control_db = ControlDb(engine=engine)



"""
Junta a chave do jwt com a classe 
"""

from domain.jwt import JwtToken

jwt = JwtToken(sing=sing)
