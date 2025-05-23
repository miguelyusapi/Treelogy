from version1.ventas.domain.entities import PedidoVenta
from typing import Protocol


class PedidoVentaRepository(Protocol):
    def save(self, pedido: PedidoVenta) -> None:
        ...
