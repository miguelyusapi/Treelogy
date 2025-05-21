from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from zoneinfo import ZoneInfo
 
# Zona horaria de Madrid para campos datetime
MADRID = ZoneInfo("Europe/Madrid")

@dataclass
class CabeceraPedidoVenta:
    num_pedido_venta: str = None
    cod_cooperativa: Optional[str] = None
    puerta: Optional[str] = None
    acuerdo_venta_asociado: Optional[str] = None
    num_pedido_laboratorio: Optional[str] = None
    fecha_pedido_farmacia: datetime = field(default_factory=lambda: datetime.now(MADRID))
    fecha_pedido_cooperativa: Optional[datetime] = None
    cod_cliente_cooperativa: Optional[str] = None
    estado_pedido: str = None

@dataclass
class LineaPedidoVenta:
    num_pedido_venta: Optional[str] = None
    num_linea_pedido_venta: Optional[int] = 0
    num_pedido_lugonet: Optional[str] = None
    num_acuerdo_venta: Optional[str] = None
    cod_articulo_cooperativa: str = None
    cantidad_solicitada: int = 0
    cantidad_bonificada: int = 0
    cantidad_confirmada: int = 0
    pvl: Decimal = Decimal('0.0')
    descuento_porcentaje: Decimal = Decimal('0.0')
    descuento_unitario: Decimal = Decimal('0.0')
    pvl_neto: Decimal = Decimal('0.0')
    cargo_cooperativo: Decimal = Decimal('0.0')

    # CAMPOS SOLO PARA COOPERATIVAS
    cod_proveedor_cooperativa: Optional[str] = None
    computa_aprovisionamiento: bool = False
    ocultar_web: bool = False
    no_unnefar: bool = False
    estado_linea_pedido: str = None


@dataclass
class PedidoVenta:
    cabecera: CabeceraPedidoVenta
    lineas: List[LineaPedidoVenta]


@dataclass
class MovimientoVenta:
    id_movimiento: str
    num_pedido_venta: str
    num_linea_pedido_venta: int
    cod_cooperativa: str
    puerta: str
    num_albaran: str
    num_linea_albaran: int
    fecha_generacion_albaran: date
    fecha_real_movimiento: date
    motivo_devolucion: Optional[str]
    cantidad: float
    cantidad_bonificada_servida: float
    lote_calculado: bool
    lote: str
    fecha_caducidad: date
    almacen_origen_pedido_integrado: str
