from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date
from decimal import Decimal
from version1.compras.domain.entities import CabeceraPedidoCompra, LineaPedidoCompra, PedidoCompra
from zoneinfo import ZoneInfo
### GRUPO PHARMA los que tienen "LECTURA" y "EDITABLE" ###
MADRID = ZoneInfo("Europe/Madrid")

# --- PHARMA LECTURA ---
# Campos que Pharma sólo puede leer (generados por Coop)
class CabeceraPedidoCompraPharmaLectura(BaseModel):
    num_pedido_compra: Optional[str]
    cod_cooperativa: Optional[str]
    puerta: Optional[str]
    cod_proveedor_cooperativa: Optional[str]
    tipo_pedido: Optional[str]
    dias_aplazamiento: Optional[int]
    pvl: Optional[Decimal]
    pvl_neto: Optional[Decimal]
    precio_libre: Optional[Decimal]
    precio_libre_neto: Optional[Decimal]
    dto_comercial: Optional[Decimal]
    dto_logistico: Optional[Decimal]
    dto_pronto_pago: Optional[Decimal]
    dto_gestion: Optional[Decimal]
    no_unnefar: Optional[bool]
    fecha_pedido: Optional[date]
    fecha_prevista_entrega: Optional[date]
    num_acuerdo_compra: Optional[str]
    estado_pedido: Optional[str]
    almacen_origen_pedido_integrado: Optional[str]
    
class LineaPedidoCompraPharmaLectura(BaseModel):
    num_pedido_compra: Optional[str]
    num_linea_pedido_compra: Optional[int]
    cod_articulo_cooperativa: Optional[str]
    cantidad_solicitada: Optional[Decimal]
    pvl: Optional[Decimal]
    pvl_neto: Optional[Decimal]
    precio_libre: Optional[Decimal]
    precio_libre_neto: Optional[Decimal]
    dto_comercial: Optional[Decimal]
    dto_logistico: Optional[Decimal]
    dto_pronto_pago: Optional[Decimal]
    dto_gestion: Optional[Decimal]
    pedido_cooperativa: Optional[str]
    estado_linea_pedido: Optional[str]
    
class PedidoCompraPharmaLecturaDTO(BaseModel):
    cabecera: CabeceraPedidoCompraPharmaLectura
    lineas: List[LineaPedidoCompraPharmaLectura]

    @classmethod
    def from_domain(cls, pedido: PedidoCompra) -> "PedidoCompraPharmaLecturaDTO":
        return cls(
            cabecera=CabeceraPedidoCompraPharmaLectura(**pedido.cabecera.__dict__),
            lineas=[LineaPedidoCompraPharmaLectura(**linea.__dict__) for linea in pedido.lineas]
        )
    
# EDITABLE - Datos generados por Farma pero modificables por Cooperativa
# --- PHARMA EDITABLE ---
# Campos que Pharma puede modificar
class CabeceraPedidoCompraPharmaEditable(BaseModel):
    cod_proveedor_cooperativa: Optional[str] = None
    estado_pedido: Optional[str] = None
    no_unnefar: Optional[bool] = None


class LineaPedidoCompraPharmaEditable(BaseModel):
    estado_linea_pedido: Optional[str] = None
    compra_id_linea: Optional[str] = None

   

class PedidoCompraPharmaEditableDTO(BaseModel):
    cabecera: CabeceraPedidoCompraPharmaEditable
    lineas: List[LineaPedidoCompraPharmaEditable]

    class Config:
        schema_extra = {
            "example": {
                "cabecera": {
                    "cod_proveedor_cooperativa": "PROV001-EJEMPLO",
                    "estado_pedido": "ABIERTO-EJEMPLO",
                    "no_unnefar": False
                },
                "lineas": [
                    {
                        "estado_linea_pedido": "ABIERTO-EJEMPLO"
                    }
                ]
            }
        }

# ESCRITURA - Campos que Farma no genera (normalmente vacíos)
class CabeceraPedidoCompraPharmaEscritura(BaseModel):
    num_pedido_compra: str
    cod_cooperativa: str  
    cod_proveedor_cooperativa: Optional[str] = None
    estado_pedido: Optional[str] = None
    puerta: Optional[str] = None
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
    fecha_pedido: Optional[date] = None
    fecha_prevista_entrega: Optional[date] = None
    num_acuerdo_compra: Optional[str] = None
    no_unnefar: Optional[bool] = False
    


class LineaPedidoCompraPharmaEscritura(BaseModel):
    num_pedido_compra: str
    num_linea_pedido_compra: int
    cod_articulo_cooperativa: str
    cantidad_solicitada: Decimal
    pvl: Optional[Decimal] = None
    pvl_neto: Optional[Decimal] = None
    precio_libre: Optional[Decimal] = None
    precio_libre_neto: Optional[Decimal] = None
    dto_comercial: Optional[Decimal] = None
    dto_logistico: Optional[Decimal] = None
    dto_pronto_pago: Optional[Decimal] = None
    dto_gestion: Optional[Decimal] = None
    estado_linea_pedido: Optional[str] = None


class PedidoCompraPharmaEscrituraDTO(BaseModel):
    cabecera: CabeceraPedidoCompraPharmaEscritura
    lineas: List[LineaPedidoCompraPharmaEscritura]

    def to_domain(self) -> PedidoCompra:
        estado_pedido = getattr(self.cabecera, "estado_pedido", None)
        if estado_pedido is None:
            estado_pedido = "ABIERTO"

        cabecera = CabeceraPedidoCompra(
            num_pedido_compra=self.cabecera.num_pedido_compra,
            cod_cooperativa=self.cabecera.cod_cooperativa,
            cod_proveedor_cooperativa=self.cabecera.cod_proveedor_cooperativa,
            estado_pedido=estado_pedido,
            puerta=self.cabecera.puerta,
            tipo_pedido=self.cabecera.tipo_pedido,
            dias_aplazamiento=self.cabecera.dias_aplazamiento,
            pvl=self.cabecera.pvl,
            pvl_neto=self.cabecera.pvl_neto,
            precio_libre=self.cabecera.precio_libre,
            precio_libre_neto=self.cabecera.precio_libre_neto,
            dto_comercial=self.cabecera.dto_comercial,
            dto_logistico=self.cabecera.dto_logistico,
            dto_pronto_pago=self.cabecera.dto_pronto_pago,
            dto_gestion=self.cabecera.dto_gestion,
            fecha_pedido=self.cabecera.fecha_pedido,
            fecha_prevista_entrega=self.cabecera.fecha_prevista_entrega,
            num_acuerdo_compra=self.cabecera.num_acuerdo_compra,
            no_unnefar=self.cabecera.no_unnefar,
        )

        lineas = []
        for linea_dto in self.lineas:
            estado_linea = getattr(linea_dto, "estado_linea_pedido", None) or None
            linea = LineaPedidoCompra(
                num_pedido_compra=linea_dto.num_pedido_compra,
                num_linea_pedido_compra=linea_dto.num_linea_pedido_compra,
                cod_articulo_cooperativa=linea_dto.cod_articulo_cooperativa,
                cantidad_solicitada=linea_dto.cantidad_solicitada,
                pvl=linea_dto.pvl,
                pvl_neto=linea_dto.pvl_neto,
                precio_libre=linea_dto.precio_libre,
                precio_libre_neto=linea_dto.precio_libre_neto,
                dto_comercial=linea_dto.dto_comercial,
                dto_logistico=linea_dto.dto_logistico,
                dto_pronto_pago=linea_dto.dto_pronto_pago,
                dto_gestion=linea_dto.dto_gestion,
                estado_linea_pedido=estado_linea,
            )
            lineas.append(linea)

        return PedidoCompra(
            cabecera=cabecera,
            lineas=lineas
        )

    class Config:
        schema_extra = {
            "example": {
                "cabecera": {
                    "num_pedido_compra": "PCP123456",
                    "cod_cooperativa": "COOP01",
                    "id_cooperativa": "IDCOOP01",
                    "cod_proveedor_cooperativa": "PROV001",
                    "estado_pedido": "ABIERTO",
                    "puerta": "P1",
                    "tipo_pedido": "C",
                    "dias_aplazamiento": 30,
                    "pvl": 1000.00,
                    "pvl_neto": 950.00,
                    "precio_libre": 1200.00,
                    "precio_libre_neto": 1150.00,
                    "dto_comercial": 5.0,
                    "dto_logistico": 2.0,
                    "dto_pronto_pago": 1.0,
                    "dto_gestion": 0.5,
                    "fecha_pedido": "2025-05-01",
                    "fecha_prevista_entrega": "2025-05-15",
                    "num_acuerdo_compra": "ACUERDO001",
                    "no_unnefar": False
                },
                "lineas": [
                    {
                        "num_pedido_compra": "PCP123456",
                        "num_linea_pedido_compra": 1,
                        "cod_articulo_cooperativa": "ART100",
                        "cantidad_solicitada": 100,
                        "pvl": 10.00,
                        "pvl_neto": 9.50,
                        "precio_libre": 12.00,
                        "precio_libre_neto": 11.50,
                        "dto_comercial": 2.0,
                        "dto_logistico": 1.0,
                        "dto_pronto_pago": 0.5,
                        "dto_gestion": 0.2,
                        "estado_linea_pedido": "ABIERTO"
                    }
                ]
            }
        }