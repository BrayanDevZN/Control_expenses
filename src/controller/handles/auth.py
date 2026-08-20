from logs.log import logger

"""
Rota que gerencia os cookie de sessão
"""

from fastapi import APIRouter, Response, Request, HTTPException
from src.domain.module import models_user
from src.service.manage import control_db, jwt

router_auth = APIRouter(prefix="/auth", tags=["auth"])


#Rota de login
@router_auth.post("/")
async def login(response:Response, user:models_user.LoginUserModel):
    try:
    
            email = models_user.ValidEmailUser(email=user.email).email
            password = models_user.ValidUserPassword(password=user.password).password
    
      
            instance_user = control_db.users.select(search="email", value=email)
    
            if instance_user is None:
    
                raise HTTPException(
                    status_code=401,
                    detail="Not found User"
                )
    
            if not hash.valid(password_hash=instance_user["password"], password=str(password)):
    
                raise HTTPException(
                    status_code=422,
                    detail="Invalid pass"
                )
    
            token = jwt.create(payload={"public_id": str(instance_user["public_id"]), "name":instance_user["name"], "role": instance_user["role"]})
    
            response.set_cookie(
                httponly=True,
                key="user_token",
                value=token,
                samesite="strict"
            )
    
            return {"status": "sucess"}
    
    
           
    except Exception as e:
    
            logger.error(e)
    
            raise HTTPException(
                detail="internal server error",
                status_code=501
            )


#Rota de logout
@router_auth.delete("/")
async def logout(response:Response):

    try:

            logger.info("Deletando cookie...")

            response.delete_cookie(key="user_token")

            return {"status": "sucess"}

    except Exception as e:

          logger.error(e)

          raise HTTPException(
                status_code=501,
                detail="internal server error"
          )




    
    

        