from app.db.supabase import supabase


def get_dashboard(tenant_id):
    drones = supabase.table("drones")\
        .select("*")\
        .eq("tenant_id", tenant_id)\
        .execute()

    logs = supabase.table("detection_logs")\
        .select("*")\
        .eq("tenant_id", tenant_id)\
        .execute()

    return {
        "total_drones": len(drones.data),
        "total_events": len(logs.data)
    }