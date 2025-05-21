from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date
from version1.compras.domain.entities import CabeceraPedidoCompra, LineaPedidoCompra, PedidoCompra

### GRUPO PHARMA los que tienen "LECTURA" y "EDITABLE" ###
class CabeceraPedidoCompraDTO(BaseModel):
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
    no_unnefar: bool                            
    fecha_pedido: date                          
    fecha_prevista_entrega: date   
    num_acuerdo_compra: str                    
    estado_pedido: str            
    
    def to_domain(self) -> CabeceraPedidoCompra:
        return CabeceraPedidoCompra(**self.dict())

class LineaPedidoCompraDTO(BaseModel):         # FK
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
    estado_linea_pedido: Optional[str] = None         

    def to_domain(self) -> LineaPedidoCompra:
        return LineaPedidoCompra(**self.dict())
    
class PedidoCompraPharmaDTO(BaseModel):
    cabecera: CabeceraPedidoCompraDTO
    lineas: List[LineaPedidoCompraDTO]

    def to_domain(self) -> PedidoCompra:
        return PedidoCompra(
            cabecera=self.cabecera.to_domain(),
            lineas=[linea.to_domain() for linea in self.lineas]
        )
    
    class Config:
        schema_extra = {
            "example": {
                "cabecera": {
                    "num_pedido_compra": "PCP123456",
                    "cod_cooperativa": "COOP001",
                    "puerta": "A1",
                    "cod_proveedor_cooperativa": "PROV001",
                    "TipoPedido": "N",
                    "dias_aplazamiento": 30,
                    "pvl": 1000.0,
                    "pvl_neto": 900.0,
                    "precio_libre": 1100.0,
                    "precio_libre_neto": 990.0,
                    "dto_comercial": 5.0,
                    "dto_logistico": 2.0,
                    "dto_pronto_pago": 1.0,
                    "dto_gestion": 0.5,
                    "no_unnefar": False,
                    "fecha_pedido": "2025-05-14",
                    "fecha_prevista_entrega": "2025-05-21",
                    "num_acuerdo_compra": "ACUERDO001",     
                    "estado_pedido": "ABIERTO",
                },
                "lineas": [
                    {
                        "num_pedido_compra": "PCP123456",
                        "num_linea_pedido_compra": 1,
                        "cod_articulo_cooperativa": "ART001",
                        "cantidad_solicitada": 10,
                        "pvl": 15.0,
                        "pvl_neto": 13.5,
                        "precio_libre": 16.0,
                        "precio_libre_neto": 14.4,
                        "dto_comercial": 1.0,
                        "dto_logistico": 0.5,
                        "dto_pronto_pago": 0.25,
                        "dto_gestion": 0.1,
                        "pedido_cooperativa": "PRV-42D",
                        "estado_linea_pedido": "ABIERTO"
                    }
                ]
            }
        }


### COOPERATIVA solo los que tienen "EDITABLE" Y "ESCRITURA" ###
class CabeceraPedidoCompraCoopDTO(BaseModel):
    cod_cliente_cooperativa: str
    estado_pedido: str    
    almacen_origen_pedido_integrado: str


class LineaPedidoCompraCoopDTO(BaseModel):
    pedido_cooperativa: Optional[str] = None
    estado_linea_pedido: Optional[str] = None

class PedidoCompraCoopDTO(BaseModel):
    cabecera: CabeceraPedidoCompraCoopDTO
    lineas: List[LineaPedidoCompraCoopDTO]

    class Config:
        schema_extra = {
            "example": {
                "cabecera": {
                    "cod_cliente_cooperativa": "CLT-0001",
                    "estado_pedido": "PENDIENTE",
                    "almacen_origen_pedido_integrado": "ALM1"
                },
                "lineas": [
                    {
                        "pedido_cooperativa": "PRV-001",
                        "estado_linea_pedido": "ABIERTO"
                    },
                    {
                        "pedido_cooperativa": "PRV-002",
                        "estado_linea_pedido": "ABIERTO"
                    }
                ]
            }
        }