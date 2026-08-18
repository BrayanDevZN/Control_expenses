"""
Junta a chave do jwt com a classe e os modulos
"""
from infra.manage import sing
import domain.module as dm

#Instancias que cuidam da criptografia
jwt = dm.JwtToken(sing=sing)
hash = dm.HashPass()
