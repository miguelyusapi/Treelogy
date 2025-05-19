from fastapi import FastAPI
from version1.ventas.adapters.api import router as ventas_router
from version1.auth.adapters.api import router as auth_router


app = FastAPI(
    title="Treelogy Middleware API",
    version="1.0.0",
    description="API para sincronizar pedidos y stock entre sistemas"
)

app.include_router(auth_router, prefix="/auth", tags=['Autenticación'])
app.include_router(ventas_router, prefix="/ventas")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
