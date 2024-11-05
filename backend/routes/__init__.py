from fastapi import APIRouter
from .form_router import router as form_router

router = APIRouter(
    prefix="/api",
)

router.include_router(form_router)
