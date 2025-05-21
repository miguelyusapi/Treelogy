from version1.ventas.adapters.dto import PedidoVentaPharmaDTO
from version1.ventas.domain.entities import PedidoVenta
from typing import Protocol

class PedidoVentaRepository(Protocol):
    def save(self, pedido: PedidoVenta) -> None:
        ...

class CreatePedidoPharmaUseCase:
    def __init__(self, repository: PedidoVentaRepository):
        self.repository = repository

    def execute(self, data: PedidoVentaPharmaDTO):
        pedido = data.to_domain()
        self.repository.save(pedido)
        return {"message": "Pedido pharma creado correctamente", "data": data}
