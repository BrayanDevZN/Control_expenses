"""
Cria os handle de users
"""

from fastapi import APIRouter, HTTPException, Cookie, Response
from service.manage import control_db, jwt, hash
from domain.module import models_user
router_users = APIRouter(prefix="/users", tags=["users"])

#Rota de criação de conta
@router_users.post("/")
async def create_user(response:Response, user:models_user.CreateUserModel):

    try:

        password = models_user.ValidUserPassword(user.password).password

        instance_user = control_db.users.insert(email=models_user.ValidEmailUser(user.email).email, password=hash.create(password=password), name=user.name)

        

      
        payload = {
            "public_id": instance_user["public_id"],
            "name": instance_user["name"],
            "role": instance_user["role"]
        }

        token = jwt.create(payload=payload)

        return response.set_cookie(
            key="user_token",
            value=token,
            httponly=True,
            samesite="strict"
            
        )

    except Exception as e:

        raise HTTPException(
            detail="error",
            status_code=501
        )

#Rota pra buscar usuario
@router_users.get("/")
async def select_user(user:models_user.LoginUserModel, response:Response):

    try:

        email = models_user.ValidEmailUser(email=user.email).email
        password = models_user.ValidUserPassword(password=user.password)

        instance_user = control_db.users.select(search=str(email))

        if instance_user is None:

            raise HTTPException(
                status_code=401,
                detail="Not found User"
            )

        if not hash.valid(password_hash=user["password"], password=password):

            raise HTTPException(
                status_code=501,
                detail="Invalid pass"
            )

        token = jwt.create(payload={"public_id": user["public_id"], "name":user["name"], "role": user["role"]})

        return response.set_cookie(
            httponly=True,
            key="user_token",
            value=token,
            samesite="strict"
        )


       
    except Exception as e:

        raise HTTPException(
            detail="error",
            status_code=501
        )


#Rota pra atualizar a senha ou nome
@router_users.patch("/")
async def update(new_password: models_user.ValidUserPassword, token: str|None = Cookie(default=None), password:str=None):

    try:
        id = int(jwt.read(token=token["user_token"])["public_id"])

        if password != None:

            if new_password != password:

                raise HTTPException(
                    detail="invalid password",
                    status_code=501
                )

        
        
        control_db.users.update(public_id=id, new_pass=hash.create(password=new_password))

        return {"status": "sucess"}

    except Exception as e:

        raise HTTPException(
            detail="error",
            status_code=501
        )


#Rota pra deletar o usuario
@router_users.delete("/{password}")
async def delete(response:Response,password:str, token:str|None = Cookie(default=None)):

    try:

        id = int(jwt.read(token=token["user_token"])["public_id"])

        control_db.users.delete(public_id=id)

        response.delete_cookie(
            key="user_token"
        )

        response.status_code = 201

        response.body = b'{"status": "sucess"}'

        return await response

    except Exception as e:

        HTTPException(
            detail="error",
            status_code=501
        )

#Rota pra logout
@router_users.delete("/logout")
def logout(response:Response):

    try:

        response.delete_cookie(key="user_token")
        response.body = b'{"status": "sucess"}'

        return response

    except Exception as e:
        raise HTTPException(
            detail="error", status_code=501
        )










        




        

        

        







        


