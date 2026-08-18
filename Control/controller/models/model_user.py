"""
cria os models de user
"""

from pydantic import field_validator, BaseModel, Field

class CreateUserModel(BaseModel):

    name:str
    email:str
    password:str
   
    
   

#Validador de senha
class ValidUserPassword(BaseModel):

    password:str

    #Valida senha
    @field_validator("password")
    def valid_pass(cls, v):
    
    
            if not any(c.issupper() for c in v):
    
                raise ValueError("Expeted upper case in password")
    
            elif not any(c.islower() for c in v):
    
                raise ValueError("Expeted lower case in password")
    
            elif not any(c.isdigit() for c in v):
    
                raise ValueError("Expeted digit in password")
    
            elif not any (c.isalpha() for c in v):
    
                raise ValueError("Expetend number in password")
    
            elif len(v) < 8:
    
                raise ValueError("Min len password is 8")
    
            return v


#Valida email
class ValidEmailUser(BaseModel):

    email:str

    @field_validator("email")
    def valid_email(cls, v):
    
            if not "@gmail.com" in v:
    
                raise ValueError("Expeted @gmail.com")
    
            return v


#Model de login
class LoginUserModel(BaseModel):

     email:str
     password:str
    


        

        
