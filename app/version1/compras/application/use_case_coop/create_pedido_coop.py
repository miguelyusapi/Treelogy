from version1.compras.adapters.dto_coop import PedidoCompraCoopEscrituraDTO
from version1.compras.application.ports import PedidoCompraRepository

class CreatePedidoCoopUseCase:
    def __init__(self, repository: PedidoCompraRepository) :
        self.repository = repository

    def execute(self, dto: PedidoCompraCoopEscrituraDTO, user: dict)-> dict:
        pedido = dto.to_domain()
        pedido.cabecera.id_cooperativa = user["id_coop"]
        self.repository.save(pedido)
        return {"message": "Pedido cooperativa creado correctamente"}