from version1.ventas.adapters.dto.dto_coop import PedidoVentaCoopEditable
from version1.ventas.application.ports import PedidoVentaRepository

class UpdatePedidoCoopUseCase:
    def __init__(self, repository: PedidoVentaRepository):
        self.repository = repository

    def execute(self, venta_id: int, data: PedidoVentaCoopEditable):
        self.repository.update_pedido_coop(venta_id, data)
        return {"message": "Pedido cooperativa actualizado correctamente"}
