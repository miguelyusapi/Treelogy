from dataclasses import dataclass
from datetime import date
from typing import List, Optional

@dataclass
class CabeceraPedidoVenta:
    num_pedido_venta: str
    cod_cooperativa: str
    puerta: str
    acuerdo_venta_asociado: str
    num_pedido_laboratorio: str
    fecha_pedido_farmacia: date
    fecha_pedido_cooperativa: date
    cod_cliente_cooperativa: str
    estado_pedido: str

@dataclass
class LineaPedidoVenta:
    num_pedido_venta: str
    num_linea_pedido_venta: int
    num_pedido_lugonet: int
    num_acuerdo_venta: int
    cod_articulo_cooperativa: str
    cantidad_solicitada: float
    cantidad_bonificada: float
    cantidad_confirmada: float
    pvl: float
    descuento_porcentaje: float
    descuento_unitario: float
    pvl_neto: float
    cargo_cooperativo: str
    cod_proveedor_cooperativa: str
    computa_aprovisionamiento: bool
    ocultar_web: bool
    no_unnefar: bool
    estado_linea_pedido: str


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
