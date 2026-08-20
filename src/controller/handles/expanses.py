from src.logs.log import logger

"""
rotas de expanses
"""

from fastapi import APIRouter, Depends, HTTPException
from src.service.manage import control_db
from src.domain.module import model_expanses
from src.controller.dependences.depends import depends

#Objeto da rota
router_expanses = APIRouter(prefix="/expanses", tags=["expanses"])


#Rota pra criar gasto
@router_expanses.post("/")
async def insert_expanses(expanse:model_expanses.validExpanse, user_id:int|None = Depends(depends)):

    try:

        #se o user id não existir, levanta erro
        if not isinstance(user_id, int):
            logger.error(str(e))
            raise user_id

        if control_db.expanses.select(name=expanse.name, user_id=user_id) is not None:
             logger.error(f"{expanse.name} exists")
          
             raise HTTPException(
                  detail=f"{expanse.name} exists"
             )

        

        
        #Cria o gasto
        result = control_db.expanses.insert(name=expanse.name, quantity=expanse.quantity, price=expanse.price)
        result["total"] = float(result["quantity"]) * result["price"]
        
        return await result

    except Exception as e:

        logger.error(e)

        raise HTTPException(status_code=501, detail="error")


#Rota pra pegar os gastos
@router_expanses.get("/")
async def select_expanses(name:str=None, user_id:int|None = Depends(depends)):

    try:

        if not isinstance(user_id, int):
                    raise user_id


        expanse = control_db.expanses.select(name=name, user_id=user_id)

        #Levanta erro se o gasto não existir
        if expanse is None:

             raise HTTPException(
                  detail=f"{name} not found" if name is not None else "not found", status_code=401
             )

        return await expanse

    except Exception as e:
         logger.error(e)

         raise HTTPException(status_code=501, detail="error")


#Rota que vai atualizar algum gasto
@router_expanses.patch("/")
async def update_expanses(expanse:model_expanses.ValidUpdateExpanses, user_id:int|None = Depends(depends)):

     try:

          if not isinstance(user_id, int):
                raise user_id


          result = control_db.expanses.update(set=expanse.set, name=expanse.name, value=expanse.value)

          result["total"] = float(result["quantity"]) * result["price"]


          return await result

     except Exception as e:
          logger.error(e)

          raise HTTPException(status_code=501, detail="error")

#Rota que vai deletar o gasto
@router_expanses.delete("/")
async def delete_expanses(user_id:int|None = Depends(depends), name:str = None):

     try:

        if not isinstance(user_id, int):
                raise user_id

        control_db.expanses.delete(user_id=user_id, name=name)

        return await {"status": "sucess"}

     except Exception as e:
          logger.error(e)

          raise HTTPException(status_code=501, detail="error")


        

          




                  


          
          

          










        
        





