from typing import List, Optional
from version1.compras.domain.entities import PedidoCompra
from version1.compras.infrastructure.sqlserver.pedido_repository import SqlServerPedidoRepository

class GetPedidosUseCase:
    def __init__(self, repository: SqlServerPedidoRepository):
        self.repository = repository

    def execute(
        self,
        cod_cooperativa: Optional[str] = None,
        estado_pedido: Optional[str] = None,
        id_cooperativa: Optional[str] = None
    ) -> List[PedidoCompra]:
        """
        Recupera pedidos de compra filtrando por:
          - cod_cooperativa
          - estado_pedido
        """
        return self.repository.get_pedidos(
            cod_cooperativa=cod_cooperativa,
            estado_pedido=estado_pedido,
            id_cooperativa=id_cooperativa      
        )