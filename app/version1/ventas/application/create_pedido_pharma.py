from version1.ventas.adapters.dto import PedidoVentaPharmaDTO
from typing import Protocol

# Definimos una interfaz de repositorio para la persistencia
class PedidoVentaRepository(Protocol):
    def save(self, pedido: PedidoVentaPharmaDTO) -> None:
        ...

# Caso de uso
class CreatePedidoPharmaUseCase:
    def __init__(self, repository: PedidoVentaRepository):
        self.repository = repository

    def execute(self, data: PedidoVentaPharmaDTO):
        self.repository.save(data)
        return {"message": "Pedido pharma creado correctamente", "data": data}
