# from fastapi import APIRouter, Depends
# from app.core.dependencies import require_role
# from app.services.user_service import create_user

# router = APIRouter()


# @router.post("/create")
# def create_user_api(data: dict, user=Depends(require_role(["admin"]))):

#     return create_user(
#         data["email"],
#         data["password"],
#         data["role"],
#         user["tenant_id"]
#     )



from fastapi import APIRouter, Depends
from app.core.dependencies import require_role
from app.services.user_service import (
    create_user,
    get_users,
    update_user_role,
    delete_user
)

router = APIRouter()


# CREATE USER (ADMIN ONLY)
@router.post("/create")
def create_user_api(data: dict, user=Depends(require_role(["admin"]))):

    return create_user(
        data["email"],
        data["password"],
        data["role"],
        user["tenant_id"]
    )


# GET USERS
@router.get("/")
def get_users_api(user=Depends(require_role(["admin"]))):

    return get_users(user["tenant_id"])


# UPDATE ROLE
@router.put("/update-role")
def update_role_api(data: dict, user=Depends(require_role(["admin"]))):

    return update_user_role(
        data["user_id"],
        data["role"]
    )


# DELETE USER
@router.delete("/delete")
def delete_user_api(data: dict, user=Depends(require_role(["admin"]))):

    return delete_user(data["user_id"])