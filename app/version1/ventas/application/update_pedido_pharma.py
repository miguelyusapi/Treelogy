from version1.ventas.adapters.dto_pharma import PedidoVentaPharmaEditable
from version1.ventas.application.ports import PedidoVentaRepository


class UpdatePedidoPharmaUseCase:
    def __init__(self, repository: PedidoVentaRepository):
        self.repository = repository

    def execute(self, venta_id: int, data: PedidoVentaPharmaEditable):
        self.repository.update_pedido_pharma(venta_id, data)
        return {"message": "Pedido pharma actualizado correctamente"}
