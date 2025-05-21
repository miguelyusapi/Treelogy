from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from version1.ventas.application.update_pedido_coop import UpdatePedidoCooperativaCommand, UpdatePedidoCooperativaHandler
from version1.ventas.application.get_pedido import GetPedidoUseCase
from version1.ventas.domain.entities import PedidoVenta
from version1.ventas.application.get_pedidos import GetPedidosUseCase
from version1.auth.application.security import get_current_user
from version1.ventas.adapters.dto import PedidoVentaPharmaDTO
from version1.ventas.application.create_pedido_pharma import CreatePedidoPharmaUseCase
from version1.ventas.infrastructure.sqlserver.pedido_repository import SqlServerPedidoRepository
from version1.ventas.adapters.dto import PedidoVentaCoopDTO
from version1.ventas.application.create_pedido_coop import CreatePedidoCoopUseCase
import os
from dotenv import load_dotenv

router = APIRouter()

load_dotenv()
CONN_STRING = os.getenv("SQLSERVER_CONN_STRING")
repo = SqlServerPedidoRepository(CONN_STRING)


@router.post("/pharma/createPedido", tags=["Ventas - Pharma"])
def create_pedido_pharma(
    data: PedidoVentaPharmaDTO = Body(...), 
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

@router.post("/coop/createPedido", tags=['Ventas - Cooperativa'])
def create_pedido_coop(
    data: PedidoVentaCoopDTO = Body(...), 
    user=Depends(get_current_user)
):
    try:
        if user["sub"] != "coop":
            raise HTTPException(status_code=403, detail="No autorizado para Cooperativa")
        
        repo = SqlServerPedidoRepository(CONN_STRING)
        use_case = CreatePedidoCoopUseCase(repo)
        return use_case.execute(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/getPedidos", response_model=List[PedidoVenta], tags=['Ventas - Obtener Pedido'])
def get_pedidos(
    cod_cooperativa: Optional[str] = Query(None),
    estado_pedido: Optional[str] = Query(None),
    user=Depends(get_current_user)
):
    use_case = GetPedidosUseCase(repo)
    return use_case.execute(
        cod_cooperativa=cod_cooperativa,
        estado_pedido=estado_pedido,
    )


@router.get("/getPedido/{venta_id}", response_model=PedidoVenta, tags=['Ventas - Obtener Pedido'])
def get_pedido(venta_id: int, user=Depends(get_current_user)):
    use_case = GetPedidoUseCase(repo)
    pedido = use_case.execute(venta_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

@router.put("/coop/updatePedido/{venta_id}", tags=['Ventas - Cooperativa'])
def update_pedido_cooperativa(
    venta_id: int = Path(..., description="ID de la venta"),
    command: UpdatePedidoCooperativaCommand = ...,
    user=Depends(get_current_user)
):
    handler = UpdatePedidoCooperativaHandler(repo)
    handler.handle(venta_id, command)
    return {"message": "Pedido actualizado correctamente"}