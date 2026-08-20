from src.infra.manage import engine

"""
junta a classe do banco com a engine
"""



from src.repository.manage import ControlDb

control_db = ControlDb(engine=engine)

