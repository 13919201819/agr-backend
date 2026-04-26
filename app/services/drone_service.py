from app.db.supabase import supabase


# CREATE DRONE
def create_drone(data, tenant_id):

    res = supabase.table("drones").insert({
        "name": data["name"],
        "model": data.get("model"),
        "serial_number": data.get("serial_number"),
        "drone_uid": data["drone_uid"],
        "location": data.get("location"),
        "tenant_id": tenant_id,
        "status": "inactive"
    }).execute()

    return res.data[0]


# GET DRONES (tenant-wise)
def get_drones(tenant_id):

    res = supabase.table("drones")\
        .select("*")\
        .eq("tenant_id", tenant_id)\
        .execute()

    return res.data


# UPDATE DRONE STATUS
def update_drone_status(drone_id, status):

    supabase.table("drones")\
        .update({"status": status})\
        .eq("id", drone_id)\
        .execute()

    return {"message": "Drone status updated"}


# DELETE DRONE
def delete_drone(drone_id):

    supabase.table("drones")\
        .delete()\
        .eq("id", drone_id)\
        .execute()

    return {"message": "Drone deleted"}