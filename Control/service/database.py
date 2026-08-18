"""
junta a classe do banco com a engine
"""


from infra.manage import engine
from repository.manage import ControlDb

control_db = ControlDb(engine=engine)