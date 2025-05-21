from version1.ventas.domain.entities import PedidoVenta
from version1.ventas.adapters.dto import PedidoVentaCoopDTO
from typing import Protocol

class PedidoVentaRepository(Protocol):
    def save(self, pedido: PedidoVenta) -> None:
        ...

class CreatePedidoCoopUseCase:
    def __init__(self, repository: PedidoVentaRepository):
        self.repository = repository

    def execute(self, data: PedidoVentaCoopDTO):
        pedido = data.to_domain()
        self.repository.save(pedido)
        return {"message": "Pedido cooperativa creado correctamente", "data": data}
