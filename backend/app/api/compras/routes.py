from fastapi import APIRouter, Path, Query
from typing import List, Optional
from datetime import date
from api.compras.schemas import PedidoCompraCreate, UpdatePedidoCompra, MovimientoCompra

router = APIRouter()


@router.post("/createPedido", summary="Crear pedido de compra completo", response_description="Confirmación de creación del pedido")
def create_order(pedido: PedidoCompraCreate):
    return {"message": "Pedido de compra creado correctamente"}


@router.get("/getPedidos", summary="Obtener listado de pedidos de compra", response_description="Listado completo de pedidos")
def get_orders():
    return {"message": "Listado de pedidos de compra"}


@router.put(
    "/updatePedido/{pedido_id}",
    summary="Actualizar un pedido de compra",
    description="Actualiza la cabecera de un pedido de compra existente.",
    response_description="Confirmación de actualización"
)
def update_order(
    pedido_id: str = Path(..., description="Número del pedido de compra a actualizar"),
    pedido_update: UpdatePedidoCompra = ...
):
    return {"message": f"Pedido de compra {pedido_id} actualizado"}


@router.get(
    "/reportMovPedido",
    response_model=List[MovimientoCompra],
    summary="Obtener reporte de movimientos de pedidos de compra",
    description="""
        Devuelve un listado de movimientos de compra registrados.  
        Se puede filtrar opcionalmente por número de pedido, cooperativa y rango de fechas de movimiento.
    """,
    response_description="Lista de movimientos de pedidos de compra"
)
def report_mov_orders(
    num_pedido_compra: Optional[str] = Query(None, description="Filtrar por número de pedido de compra"),
    cod_cooperativa: Optional[str] = Query(None, description="Filtrar por código de cooperativa"),
    fecha_desde: Optional[date] = Query(None, description="Fecha de inicio del rango de movimiento"),
    fecha_hasta: Optional[date] = Query(None, description="Fecha de fin del rango de movimiento")
):
    return [
        MovimientoCompra(
            id_movimiento="MOVC001",
            num_pedido_compra="PC-2025-001",
            num_linea_pedido_compra=1,
            num_albaran="ALBC123",
            num_linea_albaran=1,
            fecha_generacion_albaran=date(2025, 5, 12),
            fecha_real_movimiento=date(2025, 5, 13),
            cantidad=50,
            motivo_devolucion="",
            lote_calculado=True,
            lote="L456",
            fecha_caducidad=date(2026, 5, 12)
        )
    ]
