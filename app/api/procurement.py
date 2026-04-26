from fastapi import APIRouter, Depends
from app.core.dependencies import require_role
from app.services.procurement_service import (
    create_procurement,
    get_procurements,
    approve_procurement
)

router = APIRouter()


# CREATE PROCUREMENT (USER CLICK)
@router.post("/create")
def create_procurement_api(data: dict, user=Depends(require_role(["admin"]))):

    return create_procurement(data, user["tenant_id"])


# GET PROCUREMENTS
@router.get("/")
def get_procurements_api(user=Depends(require_role(["admin"]))):

    return get_procurements(user["tenant_id"])


# APPROVE PROCUREMENT
@router.post("/approve")
def approve_procurement_api(data: dict, user=Depends(require_role(["admin"]))):

    return approve_procurement(data["procurement_id"])