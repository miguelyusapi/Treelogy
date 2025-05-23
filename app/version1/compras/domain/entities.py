from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional
from decimal import Decimal
from zoneinfo import ZoneInfo

MADRID = ZoneInfo("Europe/Madrid")

@dataclass
class CabeceraPedidoCompra:
    num_pedido_compra: Optional[str] = None
    cod_cooperativa: Optional[str] = None
    puerta: Optional[str] = None
    cod_proveedor_cooperativa: Optional[str] = None
    tipo_pedido: Optional[str] = None
    dias_aplazamiento: Optional[int] = None
    pvl: Optional[Decimal] = None
    pvl_neto: Optional[Decimal] = None
    precio_libre: Optional[Decimal] = None
    precio_libre_neto: Optional[Decimal] = None
    dto_comercial: Optional[Decimal] = None
    dto_logistico: Optional[Decimal] = None
    dto_pronto_pago: Optional[Decimal] = None
    dto_gestion: Optional[Decimal] = None
    no_unnefar: bool = False
    fecha_pedido: datetime = field(default_factory=lambda: datetime.now(tz=MADRID).date())
    fecha_prevista_entrega: Optional[datetime] = None
    num_acuerdo_compra: Optional[str] = None
    estado_pedido: Optional[str] = None
    almacen_origen_pedido_integrado: Optional[str] = None
    id_cooperativa: Optional[str] = None

@dataclass
class LineaPedidoCompra:
    num_pedido_compra: Optional[str] = None
    num_linea_pedido_compra: Optional[int] = None
    cod_articulo_cooperativa: Optional[str] = None
    cantidad_solicitada: Optional[Decimal] = None
    pvl: Optional[Decimal] = None
    pvl_neto: Optional[Decimal] = None
    precio_libre: Optional[Decimal] = None
    precio_libre_neto: Optional[Decimal] = None
    dto_comercial: Optional[Decimal] = None
    dto_logistico: Optional[Decimal] = None
    dto_pronto_pago: Optional[Decimal] = None
    dto_gestion: Optional[Decimal] = None
    pedido_cooperativa: Optional[str] = None
    estado_linea_pedido: Optional[str] = None

@dataclass
class PedidoCompra:
    cabecera: CabeceraPedidoCompra
    lineas: List[LineaPedidoCompra]


@dataclass
class MovimientoCompra:
    id_movimiento: str
    num_pedido_compra: str
    num_linea_pedido_compra: int
    num_albaran: str
    num_linea_albaran: int
    fecha_generacion_albaran: datetime
    fecha_real_movimiento: datetime
    cantidad: Decimal
    motivo_devolucion: Optional[str] = None
    lote_calculado: bool = False
    lote: Optional[str] = None
    fecha_caducidad: Optional[date] = None
