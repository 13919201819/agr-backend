# from fastapi import APIRouter, Depends
# from app.core.dependencies import require_role

# router = APIRouter()


# # Admin only
# @router.post("/create")
# def create_drone(user=Depends(require_role(["admin"]))):
#     return {"message": "Drone created", "user": user}


# # Admin + Operator
# @router.get("/")
# def get_drones(user=Depends(require_role(["admin", "operator"]))):
#     return {"message": "Drone list", "user": user}


# # All roles
# @router.get("/dashboard")
# def dashboard(user=Depends(require_role(["admin", "operator", "viewer"]))):
#     return {"message": "Dashboard data", "user": user}







from fastapi import APIRouter, Depends
from app.core.dependencies import require_role
from app.services.drone_service import (
    create_drone,
    get_drones,
    update_drone_status,
    delete_drone
)

router = APIRouter()


# CREATE DRONE (ADMIN ONLY)
@router.post("/create")
def create_drone_api(data: dict, user=Depends(require_role(["admin"]))):

    return create_drone(data, user["tenant_id"])


# GET DRONES (ADMIN + OPERATOR)
@router.get("/")
def get_drones_api(user=Depends(require_role(["admin", "operator"]))):

    return get_drones(user["tenant_id"])


# UPDATE STATUS
@router.put("/status")
def update_status_api(data: dict, user=Depends(require_role(["admin", "operator"]))):

    return update_drone_status(
        data["drone_id"],
        data["status"]
    )


# DELETE DRONE (ADMIN ONLY)
@router.delete("/delete")
def delete_drone_api(data: dict, user=Depends(require_role(["admin"]))):

    return delete_drone(data["drone_id"])