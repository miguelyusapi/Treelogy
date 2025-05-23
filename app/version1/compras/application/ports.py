from version1.compras.domain.entities import PedidoCompra
from typing import Protocol


class PedidoCompraRepository(Protocol):
    def save(self, pedido: PedidoCompra) -> None:
        ...
