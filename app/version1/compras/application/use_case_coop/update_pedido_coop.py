from version1.compras.adapters.dto_coop import PedidoCompraCoopEditableDTO
from version1.compras.application.ports import PedidoCompraRepository

class UpdatePedidoCoopUseCase:
    def __init__(self, repository: PedidoCompraRepository):
        self.repository = repository

    def execute(self, venta_id: int, data: PedidoCompraCoopEditableDTO):
        self.repository.update_pedido_coop(venta_id, data)
        return {"message": "Pedido cooperativa actualizado correctamente"}
