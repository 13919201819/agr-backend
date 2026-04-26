from app.db.supabase import supabase
from app.core.security import hash_password


VALID_ROLES = ["admin", "operator", "viewer"]


# CREATE USER
def create_user(email, password, role, tenant_id):

    if role not in VALID_ROLES:
        return {"error": "Invalid role"}

    res = supabase.table("users").insert({
        "email": email,
        "password": hash_password(password),
        "role": role,
        "tenant_id": tenant_id
    }).execute()

    return res.data[0]


# GET ALL USERS (tenant-wise)
def get_users(tenant_id):

    res = supabase.table("users")\
        .select("id, email, role, status, created_at")\
        .eq("tenant_id", tenant_id)\
        .execute()

    return res.data


# UPDATE ROLE
def update_user_role(user_id, role):

    if role not in VALID_ROLES:
        return {"error": "Invalid role"}

    res = supabase.table("users")\
        .update({"role": role})\
        .eq("id", user_id)\
        .execute()

    return {"message": "Role updated"}


# DELETE USER
def delete_user(user_id):

    supabase.table("users")\
        .delete()\
        .eq("id", user_id)\
        .execute()

    return {"message": "User deleted"}