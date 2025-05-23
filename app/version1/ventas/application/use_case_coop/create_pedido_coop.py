from version1.ventas.application.ports import PedidoVentaRepository
from version1.ventas.domain.entities import PedidoVenta
from version1.ventas.adapters.dto.dto_coop import PedidoVentaCoopEscritura

class CreatePedidoCoopUseCase:
    def __init__(self, repository: PedidoVentaRepository):
        self.repository = repository

    def execute(self, dto: PedidoVentaCoopEscritura, user: dict) -> dict:
        pedido = dto.to_domain()
        pedido.cabecera.id_cooperativa = user["id_coop"]
        self.repository.save(pedido)
        return {"message": "Pedido cooperativa creado correctamente"}
