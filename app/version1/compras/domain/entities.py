from dataclasses import dataclass
from datetime import date
from typing import List, Optional

@dataclass
class CabeceraPedidoCompra:
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
    almacen_origen_pedido_integrado: Optional[str] = None

@dataclass
class LineaPedidoCompra:
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
    estado_linea_pedido: str         
    pedido_cooperativa: Optional[str] = None           


@dataclass
class PedidoCompra:
    cabecera: CabeceraPedidoCompra
    lineas: List[LineaPedidoCompra]


@dataclass
class MovimientoCompra:
    id_movimiento: str
    num_pedido_compra: str
    num_linea_pedido_compra: int
    num_albaran: str
    num_linea_albaran: int
    fecha_generacion_albaran: date
    fecha_real_movimiento: date
    cantidad: float
    motivo_devolucion: Optional[str]
    lote_calculado: bool
    lote: str
    fecha_caducidad: date
