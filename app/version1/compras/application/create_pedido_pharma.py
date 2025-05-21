from version1.compras.adapters.dto import PedidoCompraPharmaDTO
from version1.compras.domain.entities import PedidoCompra
from typing import Protocol

# Definimos una interfaz de repositorio para la persistencia
class PedidoCompraRepository(Protocol):
    def save(self, pedido: PedidoCompra) -> None:
        ...

# Caso de uso
class CreatePedidoPharmaUseCase:
    def __init__(self, repository: PedidoCompraRepository):
        self.repository = repository

    def execute(self, data: PedidoCompraPharmaDTO):
        pedido =data.to_domain()
        self.repository.save(pedido)
        return {"message": "Pedido pharma creado correctamente", "data": data}
