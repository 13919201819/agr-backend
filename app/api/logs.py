# from fastapi import APIRouter
# from app.db.supabase import supabase

# router = APIRouter()


# @router.get("/")
# def get_logs():
#     res = supabase.table("detection_logs")\
#         .select("*")\
#         .order("created_at", desc=True)\
#         .limit(50)\
#         .execute()

#     return res.data




from fastapi import APIRouter, Query
from app.db.supabase import supabase
from datetime import datetime, timedelta

router = APIRouter()


# 🔹 GET RECENT LOGS
@router.get("/")
def get_logs(
    drone_id: str = None,
    minutes: int = 60
):
    time_threshold = (datetime.utcnow() - timedelta(minutes=minutes)).isoformat()

    query = supabase.table("detection_logs")\
        .select("*")\
        .gte("created_at", time_threshold)

    if drone_id:
        query = query.eq("drone_id", drone_id)

    res = query.order("created_at", desc=True).execute()

    return res.data


# 🔹 GET STATS
@router.get("/stats")
def get_stats(minutes: int = 60):

    time_threshold = (datetime.utcnow() - timedelta(minutes=minutes)).isoformat()

    res = supabase.table("detection_logs")\
        .select("human_count, density")\
        .gte("created_at", time_threshold)\
        .execute()

    data = res.data

    if not data:
        return {"message": "No data"}

    counts = [d["human_count"] for d in data]

    avg_count = sum(counts) / len(counts)
    max_count = max(counts)

    density_counts = {
        "LOW": 0,
        "MEDIUM": 0,
        "HIGH": 0
    }

    for d in data:
        density_counts[d["density"]] += 1

    return {
        "average_humans": round(avg_count, 2),
        "peak_humans": max_count,
        "density_distribution": density_counts,
        "total_records": len(data)
    }