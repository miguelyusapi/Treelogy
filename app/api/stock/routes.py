from fastapi import APIRouter, Query
from typing import List, Optional
from datetime import date
from api.stock.schemas import MovimientoRegularizacion, ReporteStock

router = APIRouter()


@router.post("/reportRegularizacion", summary="Registrar movimiento de regularización", response_description="Confirmación de registro")
def report_regularizacion(movimiento: MovimientoRegularizacion):
    return {"message": "Movimiento de regularización recibido correctamente"}


@router.get(
    "/getRegularizacion",
    summary="Consultar movimientos de regularización",
    response_model=List[MovimientoRegularizacion],
    description="Devuelve los movimientos de regularización registrados con opción de filtros.",
    response_description="Listado de movimientos de regularización"
)
def get_regularizacion(
    cod_cooperativa: Optional[str] = Query(None, description="Código de cooperativa"),
    fecha_desde: Optional[date] = Query(None, description="Fecha mínima del movimiento"),
    fecha_hasta: Optional[date] = Query(None, description="Fecha máxima del movimiento")
):
    return [
        MovimientoRegularizacion(
            id_movimiento="MOVREG001",
            cod_cooperativa="COOP01",
            puerta="ALM01",
            fecha_real_movimiento=date(2025, 5, 13),
            cod_proveedor_cooperativa="PROV123",
            cod_articulo_cooperativa="ART001",
            cantidad=100,
            lote_calculado=True,
            lote="L999",
            fecha_caducidad=date(2026, 6, 30)
        )
    ]


@router.post("/reportStock", summary="Registrar estado de stock", response_description="Confirmación de recepción")
def report_stock(stock: ReporteStock):
    return {"message": "Reporte de stock recibido correctamente"}


@router.get(
    "/getStock",
    summary="Consultar stock actual",
    response_model=List[ReporteStock],
    description="Devuelve el stock registrado por artículo, cooperativa o almacén.",
    response_description="Listado de stock"
)
def get_stock(
    cod_cooperativa: Optional[str] = Query(None),
    puerta: Optional[str] = Query(None),
    cod_articulo_cooperativa: Optional[str] = Query(None)
):
    return [
        ReporteStock(
            cod_cooperativa="COOP01",
            puerta="ALM01",
            fecha_reporte=date(2025, 5, 13),
            cod_articulo_cooperativa="ART001",
            stock=200,
            stock_no_disponible=10,
            stock_pendiente_colocar=20,
            stock_en_curso=15
        )
    ]
