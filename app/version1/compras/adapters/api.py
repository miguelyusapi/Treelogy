from fastapi import APIRouter, Body, Depends, HTTPException
from version1.auth.application.security import get_current_user
from version1.compras.adapters.dto import PedidoCompraPharmaDTO
from version1.compras.application.create_pedido_pharma import CreatePedidoPharmaUseCase, PedidoCompraRepository
from version1.compras.infrastructure.sqlserver_pedido_repository import SqlServerPedidoRepository
from version1.compras.adapters.dto import PedidoCompraCoopDTO
from version1.compras.application.create_pedido_coop import CreatePedidoCoopUseCase

router = APIRouter()


import os
from dotenv import load_dotenv

load_dotenv()
CONN_STRING = os.getenv("SQLSERVER_CONN_STRING")
repo = SqlServerPedidoRepository(CONN_STRING)


@router.post("/pharma/createPedido", tags=["Compras - Pharma"])
def create_pedido_pharma(
    data: PedidoCompraPharmaDTO = Body(...), 
    user=Depends(get_current_user)
):
    try:
        if user["sub"] != "pharma":
            raise HTTPException(status_code=403, detail="No autorizado para Pharma")
        repo = SqlServerPedidoRepository(CONN_STRING)
        use_case = CreatePedidoPharmaUseCase(repo)
        return use_case.execute(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/coop/createPedido", tags=['Compras - Cooperativa'])
def create_pedido_coop(
    data: PedidoCompraCoopDTO = Body(...), 
    user=Depends(get_current_user)
):
    try:
        if user["sub"] != "coop":
            raise HTTPException(status_code=403, detail="No autorizado para Cooperativa")
        use_case = CreatePedidoCoopUseCase(repo)
        return use_case.execute(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))