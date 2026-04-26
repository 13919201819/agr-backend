# from app.db.supabase import supabase
# from app.core.security import create_token, hash_password, verify_password

# # SIGNUP
# def signup(email, password, organization):

#     # Check existing user
#     existing = supabase.table("users")\
#         .select("*")\
#         .eq("email", email)\
#         .execute()

#     if existing.data:
#         return {"error": "User already exists"}

#     # Create tenant
#     tenant_res = supabase.table("tenants").insert({
#         "name": organization
#     }).execute()

#     tenant = tenant_res.data[0]
#     tenant_id = tenant["id"]

#     # Create user (HASHED PASSWORD)
#     user_res = supabase.table("users").insert({
#         "email": email,
#         "password": hash_password(password),
#         "tenant_id": tenant_id,
#         "role": "admin"
#     }).execute()

#     user = user_res.data[0]

#     # Remove password
#     user.pop("password", None)

#     # Token
#     token = create_token({
#         "user_id": user["id"],
#         "tenant_id": tenant_id,
#         "role": "admin"
#     })

#     return {
#         "token": token,
#         "user": user
#     }


# # LOGIN
# def login(email, password):

#     user_res = supabase.table("users")\
#         .select("*")\
#         .eq("email", email)\
#         .execute()

#     if not user_res.data:
#         return {"error": "User not found"}

#     user = user_res.data[0]

#     # Verify hashed password
#     if not verify_password(password, user["password"]):
#         return {"error": "Invalid password"}

#     user.pop("password", None)

#     token = create_token({
#         "user_id": user["id"],
#         "tenant_id": user["tenant_id"],
#         "role": user["role"]
#     })

#     return {
#         "token": token,
#         "user": user
#     }


from app.db.supabase import supabase
from app.core.security import create_token, hash_password, verify_password
import uuid
from datetime import datetime, timedelta
from app.services.email_service import send_reset_email


# =========================
# SIGNUP
# =========================
def signup(email, password, organization):

    # Check existing user
    existing = supabase.table("users")\
        .select("*")\
        .eq("email", email)\
        .execute()

    if existing.data:
        return {"error": "User already exists"}

    # Create tenant
    tenant_res = supabase.table("tenants").insert({
        "name": organization
    }).execute()

    if not tenant_res.data:
        return {"error": "Tenant creation failed"}

    tenant = tenant_res.data[0]
    tenant_id = tenant["id"]

    # Create user (hashed password)
    user_res = supabase.table("users").insert({
        "email": email,
        "password": hash_password(password),
        "tenant_id": tenant_id,
        "role": "admin"
    }).execute()

    if not user_res.data:
        return {"error": "User creation failed"}

    user = user_res.data[0]

    # Remove password before returning
    user.pop("password", None)

    # Generate token
    token = create_token({
        "user_id": user["id"],
        "tenant_id": tenant_id,
        "role": "admin"
    })

    return {
        "token": token,
        "user": user
    }


# =========================
# LOGIN
# =========================
def login(email, password):

    user_res = supabase.table("users")\
        .select("*")\
        .eq("email", email)\
        .execute()

    if not user_res.data:
        return {"error": "User not found"}

    user = user_res.data[0]

    # Verify hashed password
    if not verify_password(password, user["password"]):
        return {"error": "Invalid password"}

    # Remove password before returning
    user.pop("password", None)

    token = create_token({
        "user_id": user["id"],
        "tenant_id": user["tenant_id"],
        "role": user["role"]
    })

    return {
        "token": token,
        "user": user
    }


# =========================
# FORGOT PASSWORD
# =========================
def forgot_password(email):

    user_res = supabase.table("users")\
        .select("*")\
        .eq("email", email)\
        .execute()

    if not user_res.data:
        return {"error": "User not found"}

    token = str(uuid.uuid4())

    supabase.table("password_resets").insert({
        "email": email,
        "token": token,
        "expires_at": (datetime.utcnow() + timedelta(minutes=15)).isoformat()
    }).execute()

    # return {
    #     "message": "Reset token generated",
    #     "reset_token": token   # ⚠️ later remove this when email is added
    # }
    
    reset_link = f"http://localhost:3000/reset-password?token={token}"

    send_reset_email(email, reset_link)

    return {
        "message": "Password reset link sent to your email"
    }


# =========================
# RESET PASSWORD
# =========================
def reset_password(token, new_password):

    reset_res = supabase.table("password_resets")\
        .select("*")\
        .eq("token", token)\
        .execute()

    if not reset_res.data:
        return {"error": "Invalid token"}

    record = reset_res.data[0]

    # Check expiry
    if datetime.utcnow() > datetime.fromisoformat(record["expires_at"]):
        return {"error": "Token expired"}

    # Update password
    supabase.table("users")\
        .update({
            "password": hash_password(new_password)
        })\
        .eq("email", record["email"])\
        .execute()

    return {"message": "Password updated successfully"}