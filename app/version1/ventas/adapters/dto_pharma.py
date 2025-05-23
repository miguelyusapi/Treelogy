from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel

from version1.ventas.domain.entities import CabeceraPedidoVenta, LineaPedidoVenta, PedidoVenta


# ==============================
# CABECERA
# ==============================
class CabeceraPedidoVentaPharmaLectura(BaseModel):
    num_pedido_venta: Optional[str]
    cod_cooperativa: Optional[str]
    puerta: Optional[str]
    acuerdo_venta_asociado: Optional[str]
    num_pedido_laboratorio: Optional[str]
    fecha_pedido_farmacia: Optional[date]
    fecha_pedido_cooperativa: Optional[date]
    cod_cliente_cooperativa: Optional[str]
    estado_pedido: Optional[str]
    id_cooperativa: Optional[str]

class CabeceraPedidoVentaPharmaEscritura(BaseModel):
    num_pedido_venta: str
    cod_cooperativa: str
    puerta: str
    acuerdo_venta_asociado: str
    num_pedido_laboratorio: str
    fecha_pedido_farmacia: date
    fecha_pedido_cooperativa: date
    cod_cliente_cooperativa: str
    estado_pedido: str

class CabeceraPedidoVentaPharmaEditable(BaseModel):
    estado_pedido: Optional[str]


# ==============================
# LÍNEA
# ==============================
class LineaPedidoVentaPharmaLectura(BaseModel):
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

class LineaPedidoVentaPharmaEscritura(BaseModel):
    num_pedido_venta: str
    num_linea_pedido_venta: int
    num_pedido_lugonet: str
    num_acuerdo_venta: str
    cod_articulo_cooperativa: str
    cantidad_solicitada: Decimal
    cantidad_bonificada: Decimal
    cantidad_confirmada: Decimal
    pvl: Decimal
    descuento_porcentaje: Decimal
    descuento_unitario: Decimal
    pvl_neto: Decimal
    cargo_cooperativo: Decimal
    estado_linea_pedido: str

class LineaPedidoVentaPharmaEditable(BaseModel):
    venta_linea_id: int
    estado_linea_pedido: Optional[str]


# ===========================================
# PEDIDO
# ===========================================
class PedidoVentaPharmaLectura(BaseModel):
    cabecera: CabeceraPedidoVentaPharmaLectura
    lineas: List[LineaPedidoVentaPharmaLectura]

    @staticmethod
    def from_domain(pedido: PedidoVenta) -> "PedidoVentaPharmaLectura":
        return PedidoVentaPharmaLectura(
            cabecera=CabeceraPedidoVentaPharmaLectura(**pedido.cabecera.__dict__),
            lineas=[LineaPedidoVentaPharmaLectura(**linea.__dict__) for linea in pedido.lineas]
        )


class PedidoVentaPharmaEscritura(BaseModel):
    cabecera: CabeceraPedidoVentaPharmaEscritura
    lineas: List[LineaPedidoVentaPharmaEscritura]

    def to_domain(self) -> PedidoVenta:
        cabecera = CabeceraPedidoVenta(**self.cabecera.dict())
        lineas = [LineaPedidoVenta(**linea.dict()) for linea in self.lineas]
        return PedidoVenta(cabecera=cabecera, lineas=lineas)
    
    class Config:
        schema_extra = {
            "example": {
                "cabecera": {
                    "num_pedido_venta": "PV12345",
                    "cod_cooperativa": "COOP001",
                    "puerta": "B",
                    "acuerdo_venta_asociado": "ACV123",
                    "num_pedido_laboratorio": "LAB789",
                    "fecha_pedido_farmacia": "2025-05-22T10:00:00",
                    "fecha_pedido_cooperativa": "2025-05-22T12:00:00",
                    "cod_cliente_cooperativa": "CLI456",
                    "estado_pedido": "ABIERTO"
                },
                "lineas": [
                    {
                        "num_pedido_venta": "PV12345",
                        "num_linea_pedido_venta": 1,
                        "num_pedido_lugonet": "LUG001",
                        "num_acuerdo_venta": "ACV123",
                        "cod_articulo_cooperativa": "ART001",
                        "cantidad_solicitada": 10,
                        "cantidad_bonificada": 2,
                        "cantidad_confirmada": 10,
                        "pvl": 15.5,
                        "descuento_porcentaje": 5.0,
                        "descuento_unitario": 0.78,
                        "pvl_neto": 14.72,
                        "cargo_cooperativo": 0.50,
                        "estado_linea_pedido": "ENVIADO"
                    }
                ]
            }
        }

class PedidoVentaPharmaEditable(BaseModel):
    cabecera: Optional[CabeceraPedidoVentaPharmaEditable] = None
    lineas: Optional[List[LineaPedidoVentaPharmaEditable]] = None
