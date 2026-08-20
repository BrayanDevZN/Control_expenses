"""
Junta a chave do jwt com a classe e os modulos
"""
from src.infra.manage import sing
import src.domain.module as dm

#Instancias que cuidam da criptografia
jwt = dm.JwtToken(sing=sing)
hash = dm.HashPass()
