from src.logs.log import logger


"""Cria os hash pra senha e compara"""

import bcrypt

class HashPass:

    #Cria o hash
    @staticmethod
    def create(password:str) -> str:

        logger.info("Codificando senha...")

        new_pass = bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())

        return new_pass.decode("utf-8")



    #Compara os a senha coma senha em hash
    @staticmethod
    def valid(password:str, password_hash:str) -> bool:

        logger.info("Comparando senhas...")

        return bcrypt.checkpw(password=password.encode(), hashed_password=password_hash.encode())






