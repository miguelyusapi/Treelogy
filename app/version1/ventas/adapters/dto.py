from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date

from version1.ventas.domain.entities import CabeceraPedidoVenta, LineaPedidoVenta, PedidoVenta

### GRUPO PHARMA ###
class CabeceraPedidoVentaDTO(BaseModel):
    num_pedido_venta: str
    cod_cooperativa: str
    puerta: str
    acuerdo_venta_asociado: str
    num_pedido_laboratorio: str
    fecha_pedido_farmacia: date
    fecha_pedido_cooperativa: Optional[date]
    cod_cliente_cooperativa: str
    estado_pedido: str

    def to_domain(self) -> CabeceraPedidoVenta:
        return CabeceraPedidoVenta(**self.dict())

class LineaPedidoVentaDTO(BaseModel):
    num_pedido_venta: str
    num_linea_pedido_venta: int
    num_pedido_lugonet: str
    num_acuerdo_venta: str
    cod_articulo_cooperativa: str
    cantidad_solicitada: float
    cantidad_bonificada: float
    cantidad_confirmada: float
    pvl: float
    descuento_porcentaje: Optional[float]
    descuento_unitario: Optional[float]
    pvl_neto: float
    cargo_cooperativo: Optional[int]
    estado_linea_pedido: str

    def to_domain(self) -> LineaPedidoVenta:
        return LineaPedidoVenta(**self.dict())

class PedidoVentaPharmaDTO(BaseModel):
    cabecera: CabeceraPedidoVentaDTO
    lineas: List[LineaPedidoVentaDTO]

    def to_domain(self) -> PedidoVenta:
        return PedidoVenta(
            cabecera=self.cabecera.to_domain(),
            lineas=[linea.to_domain() for linea in self.lineas]
        )

    class Config:
        schema_extra = {
            "example": {
                "cabecera": {
                    "num_pedido_venta": "PV123456",
                    "cod_cooperativa": "COOP001",
                    "puerta": "A1",
                    "acuerdo_venta_asociado": "ACV001",
                    "num_pedido_laboratorio": "LAB123456",
                    "fecha_pedido_farmacia": "2025-05-19",
                    "fecha_pedido_cooperativa": "2025-05-19",
                    "cod_cliente_cooperativa": "CLT001",
                    "estado_pedido": "pendiente"
                },
                "lineas": [
                    {
                        "num_pedido_venta": "PV123456",
                        "num_linea_pedido_venta": 1,
                        "num_pedido_lugonet": 1001,
                        "num_acuerdo_venta": 2001,
                        "cod_articulo_cooperativa": "ART001",
                        "cantidad_solicitada": 10,
                        "cantidad_bonificada": 1,
                        "cantidad_confirmada": 9,
                        "pvl": 15.0,
                        "descuento_porcentaje": 10.0,
                        "descuento_unitario": 1.5,
                        "pvl_neto": 13.5,
                        "cargo_cooperativo": 0,
                        "estado_linea_pedido": "confirmada"
                    }
                ]
            }
        }


### COOPERATIVA ###
class CabeceraPedidoVentaCoopDTO(BaseModel):
    cod_cliente_cooperativa: str
    estado_pedido: str

    def to_domain(self) -> CabeceraPedidoVenta:
        return CabeceraPedidoVenta(**self.dict())

class LineaPedidoVentaCoopDTO(BaseModel):
    cod_proveedor_cooperativa: str
    computa_aprovisionamiento: bool
    ocultar_web: bool
    no_unnefar: bool
    estado_linea_pedido: str

    def to_domain(self) -> LineaPedidoVenta:
        return LineaPedidoVenta(**self.dict())

class PedidoVentaCoopDTO(BaseModel):
    cabecera: CabeceraPedidoVentaCoopDTO
    lineas: List[LineaPedidoVentaCoopDTO]

    def to_domain(self) -> PedidoVenta:
        return PedidoVenta(
            cabecera=self.cabecera.to_domain(),
            lineas=[linea.to_domain() for linea in self.lineas]
        )

    class Config:
        schema_extra = {
            "example": {
                "cabecera": {
                    "cod_cliente_cooperativa": "CLT-0001",
                    "estado_pedido": "cerrado"
                },
                "lineas": [
                    {
                        "cod_proveedor_cooperativa": "PRV-001",
                        "computa_aprovisionamiento": True,
                        "ocultar_web": False,
                        "no_unnefar": True,
                        "estado_linea_pedido": "cerrado"
                    },
                    {
                        "cod_proveedor_cooperativa": "PRV-002",
                        "computa_aprovisionamiento": False,
                        "ocultar_web": True,
                        "no_unnefar": False,
                        "estado_linea_pedido": "cerrado"
                    }
                ]
            }
        }

class CabeceraPedidoVentaLecturaDTO(BaseModel):
    num_pedido_venta: str
    cod_cooperativa: str
    puerta: str
    acuerdo_venta_asociado: str
    num_pedido_laboratorio: Optional[str]
    fecha_pedido_farmacia: date
    fecha_pedido_cooperativa: date
    cod_cliente_cooperativa: Optional[str]
    estado_pedido: str


class LineaPedidoVentaLecturaDTO(BaseModel):
    num_pedido_venta: str
    num_linea_pedido_venta: int
    num_pedido_lugonet: Optional[int]
    num_acuerdo_venta: Optional[str]
    cod_articulo_cooperativa: str
    cantidad_solicitada: float
    cantidad_bonificada: float
    cantidad_confirmada: float
    pvl: float
    descuento_porcentaje: Optional[float]
    descuento_unitario: Optional[float]
    pvl_neto: float
    cargo_cooperativo: Optional[str]
    cod_proveedor_cooperativa: str
    computa_aprovisionamiento: bool
    ocultar_web: bool
    no_unnefar: bool
    estado_linea_pedido: str


class PedidoVentaLecturaDTO(BaseModel):
    cabecera: CabeceraPedidoVentaLecturaDTO
    lineas: List[LineaPedidoVentaLecturaDTO]

    @classmethod
    def from_domain(cls, pedido: PedidoVenta) -> 'PedidoVentaLecturaDTO':
        return cls(
            cabecera=CabeceraPedidoVentaLecturaDTO(**pedido.cabecera.__dict__),
            lineas=[LineaPedidoVentaLecturaDTO(**l.__dict__) for l in pedido.lineas]
        )