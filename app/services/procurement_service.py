from app.db.supabase import supabase
import uuid


# CREATE PROCUREMENT
def create_procurement(data, tenant_id):

    # get catalog item
    catalog = supabase.table("drone_catalog")\
        .select("*")\
        .eq("id", data["catalog_id"])\
        .execute()

    if not catalog.data:
        return {"error": "Invalid catalog item"}

    item = catalog.data[0]

    quantity = data.get("quantity", 1)
    total_cost = item["price"] * quantity

    res = supabase.table("drone_procurements").insert({
        "tenant_id": tenant_id,
        "catalog_id": data["catalog_id"],
        "quantity": quantity,
        "total_cost": total_cost,
        "status": "pending"
    }).execute()

    return res.data[0]


# GET PROCUREMENTS
def get_procurements(tenant_id):

    res = supabase.table("drone_procurements")\
        .select("*")\
        .eq("tenant_id", tenant_id)\
        .execute()

    return res.data


# APPROVE PROCUREMENT → CREATE DRONES
def approve_procurement(procurement_id):

    # get procurement
    res = supabase.table("drone_procurements")\
        .select("*")\
        .eq("id", procurement_id)\
        .execute()

    if not res.data:
        return {"error": "Procurement not found"}

    procurement = res.data[0]

    if procurement["status"] == "approved":
        return {"error": "Already approved"}

    # get catalog
    catalog = supabase.table("drone_catalog")\
        .select("*")\
        .eq("id", procurement["catalog_id"])\
        .execute()

    item = catalog.data[0]

    drones = []

    for i in range(procurement["quantity"]):
        drone_uid = f"{item['name']}-{uuid.uuid4().hex[:6]}"

        drone = supabase.table("drones").insert({
            "tenant_id": procurement["tenant_id"],
            "name": item["name"],
            "model": item["model"],
            "drone_uid": drone_uid,
            "status": "inactive",
            "procurement_id": procurement_id
        }).execute()

        drones.append(drone.data[0])

    # update procurement status
    supabase.table("drone_procurements")\
        .update({"status": "approved"})\
        .eq("id", procurement_id)\
        .execute()

    return {
        "message": "Procurement approved and drones created",
        "drones": drones
    }