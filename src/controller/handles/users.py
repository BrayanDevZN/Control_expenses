
from src.logs.log import logger

"""
Cria os handle de users
"""
from datetime import datetime, time, timedelta
from fastapi import APIRouter, HTTPException, Cookie, Response, Request
from src.service.manage import control_db, jwt, hash
from src.domain.module import models_user
from fastapi.responses import JSONResponse
router_users = APIRouter(prefix="/users", tags=["users"])

#Rota de criação de conta
@router_users.post("/")
async def create_user(response:Response, user:models_user.CreateUserModel):

    try:

        password = models_user.ValidUserPassword(password=user.password).password

        instance_user = control_db.users.insert(email=models_user.ValidEmailUser(email=user.email).email, password=hash.create(password=password), name=user.name, role="user")

        
        future = datetime.now() + timedelta(days=3)
      
        payload = {
            "public_id": str(instance_user["public_id"]),
            "name": instance_user["name"],
            "role": instance_user["role"],
            "expired": future.strftime("%Y-%m-%d")
        }

        token = jwt.create(payload=payload)

        response.set_cookie(
            key="user_token",
            value=token,
            httponly=True,
            samesite="strict"
            
        )

        return  {"name": instance_user["name"], "created_at": instance_user["created_at"]}

    except Exception as e:
        logger.error(e)

        raise HTTPException(
            detail="error",
            status_code=501
        )


#Rota pra atualizar a senha ou nome
@router_users.patch("/")
async def update(request:Request,response: Response, user_pass:models_user.UpdateUserModel):

    try:

        id = jwt.read(token=request.headers["X-user_token"])["public_id"]
        print(id)

        if user_pass.new_password == user_pass.password:

                return JSONResponse(
                    content={"detail":"invalid password"},
                    status_code=501
                )

        
        
        control_db.users.update(public_id=id, new_pass=hash.create(password=user_pass.new_password))

        response.delete_cookie(
            key="user_token",
            
        )

        
        return  {"status": "sucess"}

    except Exception as e:

        logger.error(e)

        raise HTTPException(
            detail="error",
            status_code=501
        )


#Rota pra deletar o usuario
@router_users.delete("/")
async def delete(response:Response,password:models_user.ValidUserPassword, request:Request):

    try:
        
        id = jwt.read(token=request.headers["X-user_token"])["public_id"]

        control_db.users.delete(public_id=id)

        response.delete_cookie(
            key="user_token"
        )

        response.status_code = 201

        response.body = b'{"status": "sucess"}'

        return  response

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            detail="error",
            status_code=501
        )









        




        

        

        







        


