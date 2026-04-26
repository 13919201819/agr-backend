from fastapi import Depends, HTTPException, Header
from app.core.security import verify_token


def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        user = verify_token(token)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")

        return user

    except:
        raise HTTPException(status_code=401, detail="Unauthorized")


def require_role(required_roles: list):
    def role_checker(user=Depends(get_current_user)):

        if user["role"] not in required_roles:
            raise HTTPException(status_code=403, detail="Access denied")

        return user

    return role_checker