from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel

from version1.ventas.domain.entities import CabeceraPedidoVenta, LineaPedidoVenta, PedidoVenta


# ==============================
# CABECERA
# ==============================
class CabeceraPedidoVentaCoopLectura(BaseModel):
    num_pedido_venta: Optional[str]
    cod_cooperativa: Optional[str]
    puerta: Optional[str]
    acuerdo_venta_asociado: Optional[str]
    num_pedido_laboratorio: Optional[str]
    fecha_pedido_farmacia: Optional[datetime]
    fecha_pedido_cooperativa: Optional[datetime]
    cod_cliente_cooperativa: Optional[str]
    estado_pedido: Optional[str]
    id_cooperativa: Optional[str]
    
class CabeceraPedidoVentaCoopEscritura(BaseModel):
    # No hay campos exclusivamente de escritura en la cabecera
    pass

class CabeceraPedidoVentaCoopEditable(BaseModel):
    cod_cliente_cooperativa: Optional[str]
    estado_pedido: Optional[str]




# ==============================
# LÍNEA
# ==============================
class LineaPedidoVentaCoopLectura(BaseModel):
    num_pedido_venta: Optional[str]  
    num_linea_pedido_venta: Optional[int]  
    num_pedido_lugonet: Optional[str]  
    num_acuerdo_venta: Optional[str]  
    cod_articulo_cooperativa: Optional[str]  
    cantidad_solicitada: Optional[Decimal]  
    cantidad_bonificada: Optional[Decimal]  
    cantidad_confirmada: Optional[Decimal]  
    pvl: Optional[Decimal]  
    descuento_porcentaje: Optional[Decimal]  
    descuento_unitario: Optional[Decimal]  
    pvl_neto: Optional[Decimal]  
    cargo_cooperativo: Optional[Decimal]  
    cod_proveedor_cooperativa: Optional[str]  
    computa_aprovisionamiento: Optional[bool]  
    ocultar_web: Optional[bool]  
    no_unnefar: Optional[bool]  
    estado_linea_pedido: Optional[str]  

class LineaPedidoVentaCoopEscritura(BaseModel):
    cod_proveedor_cooperativa: str
    computa_aprovisionamiento: bool
    ocultar_web: bool
    no_unnefar: bool

class LineaPedidoVentaCoopEditable(BaseModel):
    venta_linea_id: int
    estado_linea_pedido: Optional[str]  


# ===========================================
# PEDIDO
# ===========================================

class PedidoVentaCoopLectura(BaseModel):
    cabecera: CabeceraPedidoVentaCoopLectura
    lineas: List[LineaPedidoVentaCoopLectura]

    @staticmethod
    def from_domain(pedido: PedidoVenta) -> "PedidoVentaCoopLectura":
        return PedidoVentaCoopLectura(
            cabecera=CabeceraPedidoVentaCoopLectura(**pedido.cabecera.__dict__),
            lineas=[LineaPedidoVentaCoopLectura(**linea.__dict__) for linea in pedido.lineas]
        )



class PedidoVentaCoopEscritura(BaseModel):
    cabecera: Optional[CabeceraPedidoVentaCoopEscritura] = CabeceraPedidoVentaCoopEscritura()
    lineas: List[LineaPedidoVentaCoopEscritura] = []

    def to_domain(self) -> PedidoVenta:
        cod_cliente_cooperativa = None
        estado_pedido = None
        if self.cabecera:
            cod_cliente_cooperativa = getattr(self.cabecera, "cod_cliente_cooperativa", None)
            estado_pedido = getattr(self.cabecera, "estado_pedido", None)

        cabecera = CabeceraPedidoVenta(
            cod_cliente_cooperativa=cod_cliente_cooperativa,
            estado_pedido=estado_pedido,
        )

        lineas = [
            LineaPedidoVenta(
                cod_proveedor_cooperativa=l.cod_proveedor_cooperativa,
                computa_aprovisionamiento=l.computa_aprovisionamiento,
                ocultar_web=l.ocultar_web,
                no_unnefar=l.no_unnefar
            ) for l in self.lineas
        ]
        return PedidoVenta(cabecera=cabecera, lineas=lineas)
    
    class Config:
        schema_extra = {
            "example": {
                "cabecera": {},
                "lineas": [
                    {
                        "cod_proveedor_cooperativa": "PROV456",
                        "computa_aprovisionamiento": True,
                        "ocultar_web": False,
                        "no_unnefar": False
                    },
                    {
                        "cod_proveedor_cooperativa": "PROV789",
                        "computa_aprovisionamiento": False,
                        "ocultar_web": True,
                        "no_unnefar": True
                    }
                ]
            }
        }


class PedidoVentaCoopEditable(BaseModel):
    cabecera: Optional[CabeceraPedidoVentaCoopEditable] = None
    lineas: Optional[List[LineaPedidoVentaCoopEditable]] = None


# ===========================================
# REPORTE MOVIMIENTOS
# ===========================================
class ReporteMovimientoVentaCoopLectura(BaseModel):
    id_movimiento: Optional[int]
    num_pedido_venta: Optional[str]
    num_linea_pedido_venta: Optional[int]
    cod_cooperativa: Optional[str]
    puerta: Optional[str]
    num_albaran: Optional[str]
    num_linea_albaran: Optional[int]
    fecha_generacion_albaran: Optional[datetime]
    fecha_real_movimiento: Optional[datetime]
    motivo_devolucion: Optional[str]
    cantidad: Optional[float]
    cantidad_bonificada_servida: Optional[float]
    lote_calculado: Optional[bool]
    lote: Optional[str]
    fecha_caducidad: Optional[datetime]
    almacen_origen_pedido_integrado: Optional[str]

class ReporteMovimientoVentaCoopEscritura(BaseModel):
    id_movimiento: int
    num_albaran: Optional[str]
    num_linea_albaran: Optional[int]
    fecha_generacion_albaran: Optional[datetime]
    fecha_real_movimiento: Optional[datetime]
    motivo_devolucion: Optional[str]
    cantidad: Optional[float]
    cantidad_bonificada_servida: Optional[float]
    lote_calculado: Optional[bool]
    lote: Optional[str]
    fecha_caducidad: Optional[datetime]
    almacen_origen_pedido_integrado: Optional[str]

class ReporteMovimientoVentaCoopEditable(BaseModel):
    cod_cooperativa: Optional[str]
    puerta: Optional[str]