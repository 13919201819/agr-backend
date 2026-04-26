from fastapi import APIRouter
from app.db.supabase import supabase

router = APIRouter()

@router.get("/db-test")
def db_test():
    res = supabase.table("tenants").select("*").execute()
    return res.data