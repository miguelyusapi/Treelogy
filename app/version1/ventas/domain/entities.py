from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from zoneinfo import ZoneInfo

# Zona horaria de Madrid
MADRID = ZoneInfo("Europe/Madrid")

@dataclass
class CabeceraPedidoVenta:
    num_pedido_venta: Optional[str] = None
    cod_cooperativa: Optional[str] = None
    puerta: Optional[str] = None
    acuerdo_venta_asociado: Optional[str] = None
    num_pedido_laboratorio: Optional[str] = None
    fecha_pedido_farmacia: datetime = field(default_factory=lambda: datetime.now(MADRID))
    fecha_pedido_cooperativa: Optional[datetime] = None
    cod_cliente_cooperativa: Optional[str] = None
    estado_pedido: Optional[str] = None
    id_cooperativa: Optional[str] = None



@dataclass
class LineaPedidoVenta:
    num_pedido_venta: Optional[str] = None
    num_linea_pedido_venta: Optional[int] = None
    num_pedido_lugonet: Optional[str] = None
    num_acuerdo_venta: Optional[str] = None
    cod_articulo_cooperativa: Optional[str] = None
    cantidad_solicitada: Optional[Decimal] = None
    cantidad_bonificada: Optional[Decimal] = None
    cantidad_confirmada: Optional[Decimal] = None
    pvl: Optional[Decimal] = None
    descuento_porcentaje: Optional[Decimal] = None
    descuento_unitario: Optional[Decimal] = None
    pvl_neto: Optional[Decimal] = None
    cargo_cooperativo: Optional[Decimal] = None
    cod_proveedor_cooperativa: Optional[str] = None
    computa_aprovisionamiento: Optional[bool] = False
    ocultar_web: Optional[bool] = False
    no_unnefar: Optional[bool] = False
    estado_linea_pedido: Optional[str] = None


@dataclass
class PedidoVenta:
    cabecera: CabeceraPedidoVenta
    lineas: List[LineaPedidoVenta]
