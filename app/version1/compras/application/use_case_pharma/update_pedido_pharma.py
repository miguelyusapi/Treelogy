from version1.compras.adapters.dto_pharma import PedidoCompraPharmaEditableDTO
from version1.compras.application.ports import PedidoCompraRepository


class UpdatePedidoPharmaUseCase:
    def __init__(self, repository: PedidoCompraRepository):
        self.repository = repository

    def execute(self, venta_id: int, data: PedidoCompraPharmaEditableDTO):
        self.repository.update_pedido_pharma(venta_id, data)
        return {"message": "Pedido pharma actualizado correctamente"}
