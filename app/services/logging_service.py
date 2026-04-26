from app.db.supabase import supabase

def log_detection(drone_id, count, density):
    try:
        supabase.table("detection_logs").insert({
            "drone_id": drone_id,
            "human_count": count,
            "density": density
        }).execute()
    except Exception as e:
        print("DB Logging Error:", e)