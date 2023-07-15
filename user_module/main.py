import logging
import os
import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse
from user_module.data.database import engine
from user_module.model import model
from dotenv import load_dotenv

from user_module.exceptions.exceptions import UnicornException
from user_module.routes import user_routes
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.environ.get("LOG_FILE"))
    ]
)


logger = logging.getLogger(__name__)


model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_routes.router)


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"{exc.name}"},
    )


@app.exception_handler(Exception)
async def system_exception_handler(request: Request, exc: Exception):
    logger.error(exc, request)
    return JSONResponse(
        status_code=418,
        content={"message": f"something went wrong!"},
    )


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
