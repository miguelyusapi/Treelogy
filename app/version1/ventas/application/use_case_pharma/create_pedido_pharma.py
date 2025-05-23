from version1.ventas.adapters.dto.dto_pharma import PedidoVentaPharmaEscritura
from version1.ventas.application.ports import PedidoVentaRepository

class CreatePedidoPharmaUseCase:
    def __init__(self, repository: PedidoVentaRepository):
        self.repository = repository

    def execute(self, data: PedidoVentaPharmaEscritura):
        pedido = data.to_domain()
        self.repository.save(pedido)
        return {"message": "Pedido pharma creado correctamente", "data": data}
