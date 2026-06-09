from fastapi import APIRouter
from . import currencies
from . import root
from . import subscriptions
from . import users

router = APIRouter()

router.include_router(currencies.router)
router.include_router(root.router)
router.include_router(subscriptions.router)
router.include_router(users.router)
