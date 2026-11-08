
from fastapi import FastAPI

from .poll_controller import router as poll_router


app = FastAPI(title="Poll Service")


app.include_router(poll_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
