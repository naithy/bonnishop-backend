import uvicorn
from http import HTTPStatus
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException

from src.routes.auth.router import get_current_user
from src.routes.auth.router import router as auth_router
from src.routes.games.router import router as games_router
from src.routes.orders.router import router as orders_router
from src.routes.invoice.router import router as invoice_router
from src.routes.services.router import router as services_router

app = FastAPI(root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(games_router)
app.include_router(services_router)
app.include_router(orders_router)
app.include_router(invoice_router)


@app.get("/", status_code=HTTPStatus.OK)
async def root(user: Annotated[dict, Depends(get_current_user)]):
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
    return {"User": user}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=27016)
