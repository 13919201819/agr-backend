from fastapi import APIRouter, Depends
from app.services.analytics_service import get_dashboard
from app.core.dependencies import get_current_user

router = APIRouter()


@router.get("/")
def dashboard(user=Depends(get_current_user)):
    return get_dashboard(user["tenant_id"])