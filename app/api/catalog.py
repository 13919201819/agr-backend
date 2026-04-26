from fastapi import APIRouter, Depends
from app.core.dependencies import require_role
from app.services.catalog_service import (
    create_catalog,
    get_catalog,
    get_catalog_by_id,
    update_catalog,
    delete_catalog
)

router = APIRouter()


# CREATE (ADMIN ONLY)
@router.post("/create")
def create_catalog_api(data: dict, user=Depends(require_role(["admin"]))):
    return create_catalog(data)


# GET ALL (PUBLIC / ALL USERS)
@router.get("/")
def get_catalog_api():
    return get_catalog()


# GET SINGLE (DETAIL PAGE)
@router.get("/{catalog_id}")
def get_single_catalog_api(catalog_id: str):
    return get_catalog_by_id(catalog_id)


# UPDATE (ADMIN ONLY)
@router.put("/update")
def update_catalog_api(data: dict, user=Depends(require_role(["admin"]))):
    return update_catalog(data["catalog_id"], data)


# DELETE (ADMIN ONLY)
@router.delete("/delete")
def delete_catalog_api(data: dict, user=Depends(require_role(["admin"]))):
    return delete_catalog(data["catalog_id"])