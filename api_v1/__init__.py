from fastapi import APIRouter

from .items.views import  router as items_router
from .demo_auth.views import router as demo_auth_router

router = APIRouter()
router.include_router(items_router, prefix='/items')
router.include_router(demo_auth_router,)
