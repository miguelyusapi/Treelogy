from fastapi import FastAPI
from api.ventas.routes import router as ventas_router
from api.compras.routes import router as compras_router
from api.stock.routes import router as stock_router

app = FastAPI(
    title="Treelogy Middleware API",
    version="1.0.0",
    description="API para sincronizar pedidos y stock entre sistemas"
)

app.include_router(ventas_router, prefix="/ventas", tags=["Ventas"])
app.include_router(compras_router, prefix="/compras", tags=["Compras"])
app.include_router(stock_router, prefix="/stock", tags=["Stock"])
