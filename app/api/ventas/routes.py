from fastapi import APIRouter, Path, Query, Body
from api.ventas.schemas import PedidoVentaCreate, UpdatePedidoVenta, MovimientoVenta, CabeceraPedidoVenta
from typing import List, Optional
from datetime import date


router = APIRouter()

@router.post(
    "/createPedido", 
    summary="Crear pedido de venta completo", 
    response_description="Confirmación de creación del pedido"
)
def create_order(
    pedido: PedidoVentaCreate = Body(..., description="Estructura completa del pedido de venta")
):
    return {
        "message": "Pedido de venta creado correctamente",
    }


@router.get(
    "/getPedidos",
    response_model=List[CabeceraPedidoVenta],
    summary="Obtener listado de pedidos de venta",
    response_description="Listado completo de pedidos"
)
def get_orders():
    # Dummy return por ahora
    return []


@router.put(
    "/updatePedido/{pedido_id}",
    summary="Actualizar un pedido de venta",
    description="Actualiza la cabecera y/o las líneas de un pedido de venta existente.",
    response_description="Confirmación de actualización",
)
def update_order(
    pedido_id: str = Path(..., description="Número del pedido de venta a actualizar"),
    pedido_update: UpdatePedidoVenta = Body(..., description="Datos del pedido de venta a actualizar")
):
    return {"message": f"Pedido de venta {pedido_id} actualizado"}


@router.get(
    "/reportMovPedido",
    response_model=List[MovimientoVenta],
    summary="Obtener reporte de movimientos de pedidos",
    description="""
        Devuelve un listado de movimientos de venta registrados.  
        Se puede filtrar opcionalmente por número de pedido, cooperativa y rango de fechas de movimiento.
    """,
    response_description="Lista de movimientos de pedidos de venta"
)
def report_mov_orders(
    num_pedido_venta: Optional[str] = Query(None, description="Filtrar por número de pedido de venta"),
    cod_cooperativa: Optional[str] = Query(None, description="Filtrar por código de cooperativa"),
    fecha_desde: Optional[date] = Query(None, description="Fecha de inicio del rango de movimiento"),
    fecha_hasta: Optional[date] = Query(None, description="Fecha de fin del rango de movimiento")
):
    # Aquí iría la lógica de acceso a una BBDD.
    # Por ahora, devolvemos ejemplo estático.
    return [
        MovimientoVenta(
            id_movimiento="MOV001",
            num_albaran="ALB123",
            num_linea_albaran=1,
            fecha_generacion_albaran=date(2025, 5, 10),
            fecha_real_movimiento=date(2025, 5, 11),
            motivo_devolucion="",
            cantidad=10,
            cantidad_bonificada_servida=2,
            lote_calculado=True,
            lote="L123",
            fecha_caducidad=date(2026, 5, 10),
            almacen_origen_pedido_integrado="ALM001",
            num_pedido_venta="PV-2025-001",
            num_linea_pedido_venta=1,
            cod_cooperativa="COOP01",
            puerta="P1"
        )
    ]