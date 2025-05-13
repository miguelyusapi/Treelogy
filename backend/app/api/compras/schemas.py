from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


# Cabecera del pedido de compra
class PedidoCompraCreate(BaseModel):
    # LECTURA
    num_pedido_compra: str
    cod_cooperativa: str
    puerta: str
    cod_proveedor_cooperativa: str
    TipoPedido: str
    dias_aplazamiento: int
    pvl: float
    pvl_neto: float
    precio_libre: float
    precio_libre_neto: float
    dto_comercial: float
    dto_logistico: float
    dto_pronto_pago: float
    dto_gestion: float
    fecha_pedido: date
    fecha_prevista_entrega: Optional[date]
    num_acuerdo_compra: Optional[str]

    # EDITABLE
    no_unnefar: Optional[bool] = False
    estado_pedido: str

    # ESCRITURA
    almacen_origen_pedido_integrado: Optional[str]


# Línea del pedido de compra
class LineaPedidoCompra(BaseModel):
    # LECTURA
    num_pedido_compra: str
    num_linea_pedido_compra: int
    cod_articulo_cooperativa: str
    cantidad_solicitada: float
    pvl: float
    pvl_neto: float
    precio_libre: float
    precio_libre_neto: float
    dto_comercial: float
    dto_logistico: float
    dto_pronto_pago: float
    dto_gestion: float

    # ESCRITURA
    pedido_cooperativa: Optional[bool] = False

    # EDITABLE
    estado_linea_pedido: str


# Reporte de movimientos
class MovimientoCompra(BaseModel):
    # ESCRITURA
    id_movimiento: str
    num_albaran: str
    num_linea_albaran: int
    fecha_generacion_albaran: date
    fecha_real_movimiento: date
    cantidad: float
    motivo_devolucion: Optional[str] = ""
    lote_calculado: bool
    lote: str
    fecha_caducidad: date
    
    # LECTURA
    num_pedido_compra: str
    num_linea_pedido_compra: int



##########################################################


# ----------------------------
# INPUT DE CABECERA PARA CREAR COMPRA
# ----------------------------

class CabeceraPedidoCompraCreate(BaseModel):
    almacen_origen_pedido_integrado: str
    cod_proveedor_cooperativa: Optional[str]
    no_unnefar: Optional[str]
    estado_pedido: Optional[str]


# ----------------------------
# INPUT DE LÍNEA PARA CREAR COMPRA
# ----------------------------

class LineaPedidoCompraCreate(BaseModel):
    pedido_cooperativa: str
    estado_linea_pedido: Optional[str]

# ----------------------------
# INPUT DE MOVIMIENTO PARA CREAR COMPRA
# ----------------------------

class MovimientoCompraCreate(BaseModel):
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

# ----------------------------
# MODELO COMPLETO DE INPUT PARA CREAR COMPRA
# ----------------------------

class PedidoVentaCreate(BaseModel):
    cabecera: CabeceraPedidoCompraCreate
    lineas: List[LineaPedidoCompraCreate]
    movimientos: List[MovimientoCompraCreate]

# ----------------------------
# MODELO COMPLETO DE INPUT PARA ACTUALIZAR COMPRA
# ----------------------------
class UpdatePedidoCompra(BaseModel):
    cabecera: Optional[CabeceraPedidoCompraCreate] = Field(
        None, description="Cabecera del pedido con los campos que se desean actualizar"
    )
    lineas: Optional[List[LineaPedidoCompraCreate]] = Field(
        None, description="Lista de líneas del pedido que se desean actualizar"
    )
    movimientos: Optional[MovimientoCompraCreate] = Field(
        None, description="Movimiento del pedido con los campos que se desean actualizar"
    )


