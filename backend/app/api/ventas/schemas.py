from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

# ----------------------------
# CABECERA PEDIDO DE VENTA
# ----------------------------

class CabeceraPedidoVenta(BaseModel):
    # LECTURA
    num_pedido_venta: str
    cod_cooperativa: str
    puerta: str
    acuerdo_venta_asociado: str
    num_pedido_laboratorio: str
    fecha_pedido_farmacia: date
    fecha_pedido_cooperativa: date

    # EDITABLE
    cod_cliente_cooperativa: Optional[str]
    estado_pedido: Optional[str]


# ----------------------------
# LÍNEA DE PEDIDO DE VENTA
# ----------------------------

class LineaPedidoVenta(BaseModel):
    # LECTURA
    num_pedido_venta: str
    num_linea_pedido_venta: int
    num_pedido_lugonet: str
    num_acuerdo_venta: str
    cod_articulo_cooperativa: str
    cantidad_solicitada: float
    cantidad_bonificada: float
    cantidad_confirmada: float
    pvl: float
    descuento_porcentaje: float
    descuento_unitario: float
    pvl_neto: float
    cargo_cooperativo: str

    # ESCRITURA
    cod_proveedor_cooperativa: str
    computa_aprovisionamiento: bool
    ocultar_web: bool
    no_unnefar: bool

    # EDITABLE
    estado_linea_pedido: Optional[str]


# ----------------------------
# REPORTE DE MOVIMIENTOS
# ----------------------------

class MovimientoVenta(BaseModel):
    # ESCRITURA
    id_movimiento: str
    num_albaran: str
    num_linea_albaran: int
    fecha_generacion_albaran: date
    fecha_real_movimiento: date
    motivo_devolucion: str
    cantidad: float
    cantidad_bonificada_servida: float
    lote_calculado: bool
    lote: str
    fecha_caducidad: date
    almacen_origen_pedido_integrado: str

    # LECTURA
    num_pedido_venta: str
    num_linea_pedido_venta: int

    # EDITABLE
    cod_cooperativa: Optional[str]
    puerta: Optional[str]


###############################################################

# ----------------------------
# INPUT DE CABECERA PARA CREAR VENTA
# ----------------------------

class CabeceraPedidoVentaCreate(BaseModel):
    cod_cliente_cooperativa: Optional[str]
    estado_pedido: Optional[str]


# ----------------------------
# INPUT DE LÍNEA PARA CREAR VENTA
# ----------------------------

class LineaPedidoVentaCreate(BaseModel):
    cod_proveedor_cooperativa: str
    computa_aprovisionamiento: bool
    ocultar_web: bool
    no_unnefar: bool
    estado_linea_pedido: Optional[str]

# ----------------------------
# INPUT DE MOVIMIENTO PARA CREAR VENTA
# ----------------------------

class MovimientoVentaCreate(BaseModel):
    id_movimiento: str
    num_albaran: str
    num_linea_albaran: int
    fecha_generacion_albaran: date
    fecha_real_movimiento: date
    motivo_devolucion: str
    cantidad: float
    cantidad_bonificada_servida: float
    lote_calculado: bool
    lote: str
    fecha_caducidad: date
    almacen_origen_pedido_integrado: str

    cod_cooperativa: Optional[str]
    puerta: Optional[str]

# ----------------------------
# MODELO COMPLETO DE INPUT PARA CREAR VENTA
# ----------------------------

class PedidoVentaCreate(BaseModel):
    cabecera: CabeceraPedidoVentaCreate
    lineas: List[LineaPedidoVentaCreate]
    movimientos: List[MovimientoVentaCreate]
    

# ----------------------------
# MODELO COMPLETO DE INPUT PARA ACTUALIZAR VENTA
# ----------------------------
class UpdatePedidoVenta(BaseModel):
    cabecera: Optional[CabeceraPedidoVentaCreate] = Field(
        None, description="Cabecera de la venta con los campos que se desean actualizar"
    )
    lineas: Optional[List[LineaPedidoVentaCreate]] = Field(
        None, description="Lista de líneas de la venta que se desean actualizar"
    )
    movimientos: Optional[MovimientoVentaCreate] = Field(
        None, description="Movimiento de la venta con los campos que se desean actualizar"
    )

