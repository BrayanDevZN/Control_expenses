from logs.log import logger

"""
Rota que gerencia os cookie de sessão
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Response, Request, HTTPException, Cookie
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
            future = datetime.now() + timedelta(days=3)
    
            token = jwt.create(payload={"public_id": str(instance_user["public_id"]), 
                                        "name":instance_user["name"], 
                                        "role": instance_user["role"],
                                        "expired": future.strftime("%Y-%m-%d"),
                                        "type": "acess"
                                        }
                                        )
            
    
            response.set_cookie(
                httponly=True,
                key="user_token",
                value=token,
                samesite="strict",
                secure=True
            )


            payload_refresh = {
                        "name": instance_user["name"],
                        "type": "refresh",
                        "public_id": instance_user["public_id"]
                    }
            token_refresh = jwt.create(payload=payload_refresh)
            
            
            response.set_cookie(
                        key="user_refresh_token",
                        value=token_refresh,
                        httponly=True,
                        samesite="strict",
                        secure=True
                    )
            
    
            return {"name": instance_user["name"], "created_at": instance_user["created_at"]}
    
    
           
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
            response.delete_cookie(key="user_refresh_token")

            return {"status": "sucess"}

    except Exception as e:

          logger.error(e)

          raise HTTPException(
                status_code=501,
                detail="internal server error"
          )

#Rota pra atualizar o token
@router_auth.patch("/")
async def refresh(response:Response, user_refresh_token: str|None = Cookie(default=None), user_token:str|None = Cookie(default=None)):

      try:

            token = jwt.read(user_token)
            refresh_token = jwt.read(user_refresh_token)

            if token["public_id"] != refresh_token["public_id"]:

                  raise HTTPException(
                        status_code=422,
                        detail="Just refresh token same user"
                  )

            if refresh_token["type"] != "refresh":

                  raise HTTPException(
                        detail="not refresh token", status_code=422
                  )

            instance_user = control_db.users.select(search="public_id", value=refresh_token["public_id"])


            response.set_cookie(
                            httponly=True,
                            key="user_token",
                            value=token,
                            samesite="strict",
                            secure=True

                        )
            
            
            payload_refresh = {
                                    "name": instance_user["name"],
                                    "type": "refresh",
                                    "public_id": instance_user["public_id"]
                                }
            token_refresh = jwt.create(payload=payload_refresh)
                        
                        
            response.set_cookie(
                                    key="user_refresh_token",
                                    value=token_refresh,
                                    httponly=True,
                                    samesite="strict",
                                    secure=True
                                )

            return {"status": "sucess"}

      except Exception as e:

            logger.error(e)

            HTTPException(
                  detail="Internal server error", status_code=501
            )
                        
                




            


            

            




    
    

        