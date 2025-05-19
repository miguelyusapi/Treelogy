from version1.ventas.adapters.dto import PedidoVentaCoopDTO
from typing import Protocol


# Definimos una interfaz de repositorio para la persistencia
class PedidoVentaRepository(Protocol):
    def save(self, pedido: PedidoVentaCoopDTO) -> None:
        ...

# Caso de uso
class CreatePedidoCoopUseCase:
    def __init__(self, repository: PedidoVentaRepository):
        self.repository = repository

    def execute(self, data: PedidoVentaCoopDTO):
        self.repository.save(data)
        return {"message": "Pedido cooperativa creado correctamente", "data": data}
