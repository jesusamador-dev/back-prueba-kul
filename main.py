import os
from urllib.request import Request

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.presentation.middlewares.setup_exception_handlers import setup_exception_handlers
from src.presentation.middlewares.standardize_response_middleware import standardize_response
from src.presentation.routers.transactions_routes import router as transactions_router
from src.presentation.routers.keys_routes import router as keys_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://front-prueba-kul.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_exception_handlers(app)
app.middleware("http")(standardize_response)
app.include_router(transactions_router, prefix="/v1")
app.include_router(keys_router, prefix="/v1")


# Punto de entrada
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # Railway asigna un puerto automáticamente
    uvicorn.run(app, host="0.0.0.0", port=port)
