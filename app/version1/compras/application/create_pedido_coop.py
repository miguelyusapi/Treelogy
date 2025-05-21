from version1.compras.adapters.dto import PedidoCompraCoopDTO
from typing import Protocol


# Definimos una interfaz de repositorio para la persistencia
class PedidoCompraRepository(Protocol):
    def save(self, pedido: PedidoCompraCoopDTO) -> None:
        ...

# Caso de uso
class CreatePedidoCoopUseCase:
    def __init__(self, repository: PedidoCompraRepository):
        self.repository = repository

    def execute(self, data: PedidoCompraCoopDTO):
        self.repository.save(data)
        return {"message": "Pedido cooperativa creado correctamente", "data": data}
