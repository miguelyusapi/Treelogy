from typing import List
from pydantic import BaseModel

from version1.ventas.infrastructure.sqlserver.pedido_repository import SqlServerPedidoRepository


class LineaUpdateDTO(BaseModel):
    venta_linea_id: int
    estado_linea_pedido: str


class UpdatePedidoCooperativaCommand(BaseModel):
    cod_cliente_cooperativa: str
    estado_pedido: str
    lineas: List[LineaUpdateDTO]


class UpdatePedidoCooperativaHandler:
    def __init__(self, repository: SqlServerPedidoRepository):
        self.repository = repository

    def handle(self, venta_id: int, command: UpdatePedidoCooperativaCommand):
        self.repository.update_pedido_cooperativa(venta_id, command)
