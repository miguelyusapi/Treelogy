from typing import Optional
from version1.compras.domain.entities import PedidoCompra
from version1.compras.infrastructure.sqlserver.pedido_repository import SqlServerPedidoRepository

class GetPedidoUseCase:
    def __init__(self, repository: SqlServerPedidoRepository):
        self.repository = repository

    def execute(self, compra_id: int) -> Optional[PedidoCompra]:
        """
        Recupera un pedido de compra por su ID interno (compra_id).
        """
        if compra_id <= 0:
            raise ValueError(f"compra_id inválido: {compra_id}")
        pedido: Optional[PedidoCompra] = self.repository.get_pedido(compra_id)
        if not pedido:
            return None
        return pedido
    