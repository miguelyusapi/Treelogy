from version1.compras.adapters.dto_pharma import PedidoCompraPharmaEscrituraDTO
from version1.compras.application.ports import PedidoCompraRepository

# Import or define PedidoCompraRepository


class CreatePedidoPharmaUseCase:
    def __init__(self, repository: PedidoCompraRepository) :
        self.repository = repository

    def execute(self, data: PedidoCompraPharmaEscrituraDTO):
        pedido = data.to_domain()
        self.repository.save(pedido)
        return {"message": "Pedido pharma creado correctamente"}
