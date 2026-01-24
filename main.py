from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.models.mongo_db.database import mongodb
from api_v1.products.views import router as products_router
from core.config import settings
import uvicorn

from api_v1 import router as router_v1

@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongodb.connect()

    yield

    await mongodb.disconnect()





app = FastAPI(lifespan=lifespan)
app.include_router(router= router_v1, prefix=settings.api_v1_prefix)

@app.get("/")
def hello_index():
    return {
        "message": "Hello index!",
    }




if __name__ == '__main__':

    uvicorn.run("main:app", reload=True)
