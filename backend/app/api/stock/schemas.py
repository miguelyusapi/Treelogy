from pydantic import BaseModel
from typing import Optional
from datetime import date


# Movimiento de regularización de stock
class MovimientoRegularizacion(BaseModel):
    id_movimiento: str
    cod_cooperativa: str
    puerta: str
    fecha_real_movimiento: date
    cod_proveedor_cooperativa: str
    cod_articulo_cooperativa: str
    cantidad: float
    lote_calculado: bool
    lote: str
    fecha_caducidad: date


# Reporte de stock
class ReporteStock(BaseModel):
    cod_cooperativa: str
    puerta: str
    fecha_reporte: date
    cod_articulo_cooperativa: str
    stock: float
    stock_no_disponible: float
    stock_pendiente_colocar: float
    stock_en_curso: float
