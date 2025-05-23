from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date
from decimal import Decimal
from version1.compras.domain.entities import CabeceraPedidoCompra, LineaPedidoCompra, PedidoCompra
from zoneinfo import ZoneInfo
### COOPERATIVA solo los que tienen "EDITABLE" Y "ESCRITURA" ###
MADRID = ZoneInfo("Europe/Madrid")

# LECTURA - Campos generados por Farma (opcional para Coop)
# --- COOP LECTURA ---
# Campos que Coop sólo puede leer (generados por Pharma)
class CabeceraPedidoCompraCoopLectura(BaseModel):
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

class LineaPedidoCompraCoopLectura(BaseModel):
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

class PedidoCompraCoopLecturaDTO(BaseModel):
    cabecera: CabeceraPedidoCompraCoopLectura
    lineas: List[LineaPedidoCompraCoopLectura]

    @classmethod
    def from_domain(cls, pedido: PedidoCompra) -> "PedidoCompraCoopLecturaDTO":
        return cls(
            cabecera=CabeceraPedidoCompraCoopLectura(**pedido.cabecera.__dict__),
            lineas=[LineaPedidoCompraCoopLectura(**linea.__dict__) for linea in pedido.lineas]
        )


# EDITABLE - Campos modificables por Coop
# --- COOP EDITABLE ---
# Campos que Coop puede modificar
class CabeceraPedidoCompraCoopEditable(BaseModel):
    cod_proveedor_cooperativa: Optional[str] = None
    estado_pedido: Optional[str] = None
    no_unnefar: Optional[bool] = None
    almacen_origen_pedido_integrado : Optional[str] = None



class LineaPedidoCompraCoopEditable(BaseModel):
    estado_linea_pedido: Optional[str] = None
    compra_id_linea: Optional[str] = None
    pedido_cooperativa: Optional[str] = None

   

class PedidoCompraCoopEditableDTO(BaseModel):
    cabecera: CabeceraPedidoCompraCoopEditable
    lineas: List[LineaPedidoCompraCoopEditable]

    class Config:
        schema_extra = {
            "example": {
                "cabecera": {
                    "cod_proveedor_cooperativa": "PROVCOOP01-EJEMPLO",
                    "estado_pedido": "ABIERTO-EJEMPLO",
                    "no_unnefar": False,
                    "almacen_origen_pedido_integrado": "ALM1-EJEMPLO"
                },
                "lineas": [
                    {
                        "estado_linea_pedido": "ABIERTO-EJEMPLO",
                        "pedido_cooperativa": "PCOOP100-EJEMPLO",
                    }
                ]
            }
        }

# ESCRITURA - Campos generados por Coop (pedidos, lineas)


# ESCRITURA - Campos generados por Coop (recepciones, movimientos)
class CabeceraPedidoCompraCoopEscritura(BaseModel):
    almacen_origen_pedido_integrado: str


class LineaPedidoCompraCoopEscritura(BaseModel):
    pedido_cooperativa: str


class PedidoCompraCoopEscrituraDTO(BaseModel):
    cabecera: CabeceraPedidoCompraCoopEscritura
    lineas: List[LineaPedidoCompraCoopEscritura]

    def to_domain(self) -> PedidoCompra:
    # Forzamos valores por defecto para evitar NULL en BD
        cod_cliente_cooperativa = getattr(self.cabecera, "id_cooperativa", None)
        estado_pedido = getattr(self.cabecera, "estado_pedido", None)

        cabecera = CabeceraPedidoCompra(
            num_pedido_compra=None,
            cod_cooperativa=None,
            almacen_origen_pedido_integrado=self.cabecera.almacen_origen_pedido_integrado,
            id_cooperativa=cod_cliente_cooperativa,
            estado_pedido=estado_pedido,
        )

        lineas = []
        for linea_dto in self.lineas:
            # Asignamos estado_linea_pedido por defecto para evitar NULL
            estado_linea = getattr(linea_dto, "estado_linea_pedido", None)
            linea = LineaPedidoCompra(
                num_pedido_compra=None,
                num_linea_pedido_compra=None,
                pedido_cooperativa=linea_dto.pedido_cooperativa,
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
                    "almacen_origen_pedido_integrado": "ALM1",
                },
                "lineas": [
                    {
                        "pedido_cooperativa": "PCOOP100",
                    }
                ]
            }
        }