from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date, datetime
from decimal import Decimal
from version1.compras.domain.entities import CabeceraPedidoCompra, LineaPedidoCompra, PedidoCompra
from zoneinfo import ZoneInfo

MADRID = ZoneInfo("Europe/Madrid")

### GRUPO PHARMA los que tienen "LECTURA" y "EDITABLE" ###
class CabeceraPedidoCompraDTO(BaseModel):
    num_pedido_compra: str                            
    cod_cooperativa: str                         
    puerta: Optional[str] = None                                 
    cod_proveedor_cooperativa: str  
    tipo_pedido: str                               
    dias_aplazamiento: int          
    pvl: Decimal                       
    pvl_neto: Decimal                  
    precio_libre: Decimal             
    precio_libre_neto: Decimal       
    dto_comercial: Decimal = None     
    dto_logistico: Decimal = None        
    dto_pronto_pago: Decimal = None        
    dto_gestion: Decimal = None              
    no_unnefar: bool = False                          
    fecha_pedido: date = Field(default_factory=lambda: datetime.now(tz=MADRID).date())                          
    fecha_prevista_entrega: Optional[date] = None  
    num_acuerdo_compra: Optional[str] = None                    
    estado_pedido: str            
    
    def to_domain(self) -> CabeceraPedidoCompra:
        return CabeceraPedidoCompra(**self.dict())

class LineaPedidoCompraDTO(BaseModel):      
    num_pedido_compra: str                    
    num_linea_pedido_compra: int                    
    cod_articulo_cooperativa: str                    
    cantidad_solicitada: Decimal       
    pvl: Decimal                          
    pvl_neto: Decimal               
    precio_libre: Decimal            
    precio_libre_neto: Decimal            
    dto_comercial: Decimal = None          
    dto_logistico: Decimal = None                
    dto_pronto_pago: Decimal = None             
    dto_gestion: Decimal = None              
    estado_linea_pedido: str        

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
                    "tipo_pedido": "N",
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
    num_pedido_compra: str
    cod_proveedor_cooperativa: str
    estado_pedido: str    
    almacen_origen_pedido_integrado: str          
    cod_cooperativa: str   

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
    no_unnefar: Optional[bool] = False                          
    fecha_pedido: Optional[date] = Field(default_factory=lambda: datetime.now(tz=MADRID).date())                       
    fecha_prevista_entrega: Optional[date] = None  
    num_acuerdo_compra: Optional[str] = None                    
    estado_pedido: Optional[str] = None             

    def to_domain(self) -> CabeceraPedidoCompra:
        return CabeceraPedidoCompra(**self.dict())

class LineaPedidoCompraCoopDTO(BaseModel):
    num_linea_pedido_compra: str
    pedido_cooperativa: Optional[str] = None

    num_pedido_compra: str                                    
    cod_articulo_cooperativa: str                    
    cantidad_solicitada: Decimal       
    pvl: Decimal                          
    pvl_neto: Decimal               
    precio_libre: Decimal            
    precio_libre_neto: Decimal            
    dto_comercial: Decimal = None            
    dto_logistico: Decimal = None              
    dto_pronto_pago: Decimal = None             
    dto_gestion: Decimal = None               
    estado_linea_pedido: str        
    

    def to_domain(self) -> LineaPedidoCompra:
        return LineaPedidoCompra(**self.dict())
    
class PedidoCompraCoopDTO(BaseModel):
    cabecera: CabeceraPedidoCompraCoopDTO
    lineas: List[LineaPedidoCompraCoopDTO]

    def to_domain(self) -> PedidoCompra:
        return PedidoCompra(
            cabecera=self.cabecera.to_domain(),
            lineas=[linea.to_domain() for linea in self.lineas]
        )
    
    class Config:
        schema_extra = {
            "example": {
                "cabecera": {
                    "num_pedido_compra": "PCP431",
                    "cod_proveedor_cooperativa": "CLICOOP01",
                    "estado_pedido": "ABIERTO",
                    "almacen_origen_pedido_integrado": "ALM1",
                    "cod_cooperativa": "COOP1",
                    "puerta": "A1",
                    "tipo_pedido": "N",
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
                    "num_acuerdo_compra": "ACUERDO001"
                },
                "lineas": [
                    {
                        "num_linea_pedido_compra": "1",
                        "pedido_cooperativa": "PCOOP001",
                        "num_pedido_compra": "PCP001",
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
                        "estado_linea_pedido": "ABIERTO"
                    },
                    {
                        "num_linea_pedido_compra": "2",
                        "pedido_cooperativa": "PCOOP002",
                        "num_pedido_compra": "PCP001",
                        "cod_articulo_cooperativa": "ART002",
                        "cantidad_solicitada": 5,
                        "pvl": 20.0,
                        "pvl_neto": 18.0,
                        "precio_libre": 22.0,
                        "precio_libre_neto": 19.8,
                        "dto_comercial": 0.5,
                        "dto_logistico": 0.2,
                        "dto_pronto_pago": 0.1,
                        "dto_gestion": 0.05,
                        "estado_linea_pedido": "ABIERTO"
                    }
                ]
            }
        }


