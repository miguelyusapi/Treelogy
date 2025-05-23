from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from version1.ventas.application.update_pedido_pharma import UpdatePedidoPharmaUseCase
from version1.ventas.application.update_pedido_coop import UpdatePedidoCoopUseCase
from version1.ventas.application.get_pedido import GetPedidoUseCase
from version1.ventas.application.get_pedidos import GetPedidosUseCase
from version1.ventas.application.create_pedido_pharma import CreatePedidoPharmaUseCase
from version1.ventas.adapters.dto_pharma import PedidoVentaPharmaEditable, PedidoVentaPharmaEscritura, PedidoVentaPharmaLectura
from version1.auth.application.security import get_current_user
from version1.ventas.adapters.dto_coop import PedidoVentaCoopEditable, PedidoVentaCoopEscritura, PedidoVentaCoopLectura
from version1.ventas.infrastructure.sqlserver.pedido_repository import SqlServerPedidoRepository
from version1.ventas.application.create_pedido_coop import CreatePedidoCoopUseCase
from dotenv import load_dotenv
import os

router = APIRouter()

load_dotenv()
CONN_STRING = os.getenv("SQLSERVER_CONN_STRING")
repo = SqlServerPedidoRepository(CONN_STRING)


@router.post("/pharma/createPedido", tags=["Ventas - Pharma"])
def create_pedido_pharma(
    data: PedidoVentaPharmaEscritura = Body(...), 
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
    data: PedidoVentaCoopEscritura = Body(...), 
    user=Depends(get_current_user)
):
    try:
        if user["sub"] != "coop":
            raise HTTPException(status_code=403, detail="No autorizado para Cooperativa")
        use_case = CreatePedidoCoopUseCase(repo)
        return use_case.execute(data, user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/getPedidos", tags=['Ventas - Obtener Pedidos'])
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
            return [PedidoVentaPharmaLectura.from_domain(p) for p in pedidos]
        elif user["sub"] == "coop":
            return [PedidoVentaCoopLectura.from_domain(p) for p in pedidos]
        else:
            raise HTTPException(status_code=403, detail="Rol no autorizado")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/getPedido/{venta_id}", tags=['Ventas - Obtener Pedidos'])
def get_pedido(venta_id: int, user=Depends(get_current_user)):
    try:
        use_case = GetPedidoUseCase(repo)
        pedido = use_case.execute(venta_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        if user["sub"] == "pharma":
            return PedidoVentaPharmaLectura.from_domain(pedido)
        elif user["sub"] == "coop":
            return PedidoVentaCoopLectura.from_domain(pedido)
        else:
            raise HTTPException(status_code=403, detail="Rol no autorizado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/coop/updatePedido/{venta_id}", tags=['Ventas - Cooperativa'])
def update_pedido_coop(
    venta_id: int,
    data: PedidoVentaCoopEditable = Body(...),
    user=Depends(get_current_user)
):
    if user["sub"] != "coop":
        raise HTTPException(status_code=403, detail="No autorizado para Cooperativas")

    try:
        use_case = UpdatePedidoCoopUseCase(repository=repo)
        return use_case.execute(venta_id, data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/pharma/updatePedido/{venta_id}", tags=['Ventas - Pharma'])
def update_pedido_pharma(
    venta_id: int,
    data: PedidoVentaPharmaEditable = Body(...),
    user=Depends(get_current_user)
):
    if user["sub"] != "pharma":
        raise HTTPException(status_code=403, detail="No autorizado para Pharma")

    try:
        use_case = UpdatePedidoPharmaUseCase(repository=repo)
        return use_case.execute(venta_id, data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))