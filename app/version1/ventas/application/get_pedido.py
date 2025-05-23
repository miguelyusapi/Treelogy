from typing import Optional
from version1.ventas.domain.entities import PedidoVenta
from version1.ventas.infrastructure.sqlserver.pedido_repository import SqlServerPedidoRepository

class GetPedidoUseCase:
    def __init__(self, repository: SqlServerPedidoRepository):
        self.repository = repository

    def execute(self, venta_id: int) -> PedidoVenta:
        pedido: Optional[PedidoVenta] = self.repository.get_pedido(venta_id)
        if not pedido:
            return None
        return pedido
