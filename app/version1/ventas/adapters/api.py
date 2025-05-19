from fastapi import APIRouter, Body, Depends, HTTPException
from version1.auth.application.security import get_current_user
from version1.ventas.adapters.dto import PedidoVentaPharmaDTO
from version1.ventas.application.create_pedido_pharma import CreatePedidoPharmaUseCase, PedidoVentaRepository
from version1.ventas.infrastructure.sqlserver_pedido_repository import SqlServerPedidoRepository
from version1.ventas.adapters.dto import PedidoVentaCoopDTO
from version1.ventas.application.create_pedido_coop import CreatePedidoCoopUseCase

router = APIRouter()

# repo = SqlServerPedidoRepository("Driver={ODBC Driver 18 for SQL Server};Server=localhost;Database=mi_base;UID=usuario;PWD=contraseña;")

############# PROVISIONAL PARA HACER PRUEBAS #############
class DummyPedidoRepository(PedidoVentaRepository):
    def save(self, pedido):
        print("Pedido guardado (dummy)")

repo = DummyPedidoRepository()
##########################################################


@router.post("/pharma/createPedido", tags=["Ventas - Pharma"])
def create_pedido_pharma(
    data: PedidoVentaPharmaDTO = Body(...), 
    user=Depends(get_current_user)
):
    try:
        if user["sub"] != "pharma":
            raise HTTPException(status_code=403, detail="No autorizado para Pharma")
        use_case = CreatePedidoPharmaUseCase(repo)
        return use_case.execute(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/coop/createPedido", tags=['Ventas - Cooperativa'])
def create_pedido_coop(
    data: PedidoVentaCoopDTO = Body(...), 
    user=Depends(get_current_user)
):
    try:
        if user["sub"] != "coop":
            raise HTTPException(status_code=403, detail="No autorizado para Cooperativa")
        use_case = CreatePedidoCoopUseCase(repo)
        return use_case.execute(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))