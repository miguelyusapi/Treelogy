from typing import Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from version1.compras.application.get_pedido import GetPedidoUseCase
from version1.compras.adapters.dto_pharma import PedidoCompraPharmaLecturaDTO
from version1.compras.application.get_pedidos import GetPedidosUseCase
from version1.compras.adapters.dto_coop import PedidoCompraCoopEscrituraDTO, PedidoCompraCoopLecturaDTO
from version1.auth.application.security import get_current_user
from version1.compras.adapters.dto_pharma import PedidoCompraPharmaEscrituraDTO,PedidoCompraPharmaEditableDTO
from version1.compras.adapters.dto_coop import PedidoCompraCoopEditableDTO
from version1.compras.application.use_case_pharma.create_pedido_pharma import CreatePedidoPharmaUseCase
from version1.compras.infrastructure.sqlserver.pedido_repository import SqlServerPedidoRepository
from version1.compras.application.use_case_coop.create_pedido_coop import CreatePedidoCoopUseCase
from version1.compras.application.use_case_coop.update_pedido_coop import UpdatePedidoCoopUseCase
from version1.compras.application.use_case_pharma.update_pedido_pharma import UpdatePedidoPharmaUseCase

router = APIRouter()

import os
from dotenv import load_dotenv

load_dotenv()
CONN_STRING = os.getenv("SQLSERVER_CONN_STRING")
repo = SqlServerPedidoRepository(CONN_STRING)


@router.post("/pharma/createPedido", tags=["Compras - Pharma"])
def create_pedido_pharma(
    data: PedidoCompraPharmaEscrituraDTO = Body(...), 
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
    data: PedidoCompraCoopEscrituraDTO = Body(...), 
    user=Depends(get_current_user)
):
    try:
        if user["sub"] != "coop":
            raise HTTPException(status_code=403, detail="No autorizado para Cooperativa")
        use_case = CreatePedidoCoopUseCase(repo)
        return use_case.execute(data, user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/coop/updatePedido/{compra_id}", tags=['Compras - Cooperativa'])
def update_pedido_coop(
    compra_id: int,
    data: PedidoCompraCoopEditableDTO = Body(...),
    user=Depends(get_current_user)
):
    if user["sub"] != "coop":
        raise HTTPException(status_code=403, detail="No autorizado para Cooperativas")

    try:
        use_case = UpdatePedidoCoopUseCase(repository=repo)
        return use_case.execute(compra_id, data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/pharma/updatePedido/{compra_id}", tags=['Compras - Pharma'])
def update_pedido_pharma(
    compra_id: int,
    data: PedidoCompraPharmaEditableDTO = Body(...),
    user=Depends(get_current_user)
):
    if user["sub"] != "pharma":
        raise HTTPException(status_code=403, detail="No autorizado para Pharma")

    try:
        use_case = UpdatePedidoPharmaUseCase(repository=repo)
        return use_case.execute(compra_id, data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/getPedidos", tags=['Compras - Obtener Pedidos'])
def get_pedidos(
    cod_cooperativa: Optional[str] = Query(None),
    estado_pedido: Optional[str] = Query(None),
    id_cooperativa: Optional[str] = Query(None),
    user=Depends(get_current_user)
):
    try:
        use_case = GetPedidosUseCase(repo)
        pedidos = use_case.execute(
            cod_cooperativa=cod_cooperativa,
            estado_pedido=estado_pedido,
            id_cooperativa=id_cooperativa
        )

        # Adaptamos al DTO correspondiente
        if user["sub"] == "pharma":
            return [PedidoCompraPharmaLecturaDTO.from_domain(p) for p in pedidos]
        elif user["sub"] == "coop":
            return [PedidoCompraCoopLecturaDTO.from_domain(p) for p in pedidos]
        else:
            raise HTTPException(status_code=403, detail="Rol no autorizado")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/getPedido/{compra_id}", tags=['Compras - Obtener Pedidos'])
def get_pedido(compra_id: int, user=Depends(get_current_user)):
    try:
        use_case = GetPedidoUseCase(repo)
        pedido = use_case.execute(compra_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        if user["sub"] == "pharma":
            return PedidoCompraPharmaLecturaDTO.from_domain(pedido)
        elif user["sub"] == "coop":
            return PedidoCompraCoopLecturaDTO.from_domain(pedido)
        else:
            raise HTTPException(status_code=403, detail="Rol no autorizado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))