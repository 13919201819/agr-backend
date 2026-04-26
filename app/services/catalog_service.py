# from app.db.supabase import supabase


# # CREATE PRODUCT
# # def create_catalog(data):

# #     res = supabase.table("drone_catalog").insert({
# #         "name": data["name"],
# #         "model": data.get("model"),
# #         "price": data["price"],
# #         "encryption": data.get("encryption"),
# #         "wind_resistance": data.get("wind_resistance"),
# #         "features": data.get("features", []),
# #         "specs": data.get("specs", {})
# #     }).execute()

# #     return res.data[0]

# def create_catalog(data):
    
#     res = supabase.table("drone_catalog").insert({
#         "name": data["name"],
#         "model": data.get("model"),
#         "price": data["price"],

#         "tagline": data.get("tagline"),
#         "image_url": data.get("image_url"),

#         "unit_id": data.get("unit_id"),
#         "system_auth": data.get("system_auth"),
#         "description": data.get("description"),

#         "encryption": data.get("encryption"),
#         "wind_resistance": data.get("wind_resistance"),

#         "features": data.get("features", []),

#         "range": data.get("range"),
#         "link": data.get("link"),
#         "sensors": data.get("sensors"),
#         "wind": data.get("wind")

#     }).execute()

#     return res.data[0]


# # GET ALL PRODUCTS (FOR UI)
# def get_catalog():

#     res = supabase.table("drone_catalog")\
#         .select("*")\
#         .execute()

#     return res.data


# # UPDATE PRODUCT
# def update_catalog(catalog_id, data):

#     supabase.table("drone_catalog")\
#         .update(data)\
#         .eq("id", catalog_id)\
#         .execute()

#     return {"message": "Catalog updated"}


# # DELETE PRODUCT
# def delete_catalog(catalog_id):

#     supabase.table("drone_catalog")\
#         .delete()\
#         .eq("id", catalog_id)\
#         .execute()

#     return {"message": "Catalog deleted"}


from app.db.supabase import supabase


# CREATE
def create_catalog(data):

    res = supabase.table("drone_catalog").insert({
        "name": data["name"],
        "model": data.get("model"),
        "price": data["price"],

        "tagline": data.get("tagline"),
        "image_url": data.get("image_url"),

        "unit_id": data.get("unit_id"),
        "system_auth": data.get("system_auth"),
        "description": data.get("description"),

        "encryption": data.get("encryption"),
        "wind_resistance": data.get("wind_resistance"),

        "features": data.get("features", []),

        "range": data.get("range"),
        "link": data.get("link"),
        "sensors": data.get("sensors"),
        "wind": data.get("wind")

    }).execute()

    return res.data[0]


# GET ALL
def get_catalog():
    res = supabase.table("drone_catalog").select("*").execute()
    return res.data


# GET SINGLE
def get_catalog_by_id(catalog_id):

    res = supabase.table("drone_catalog")\
        .select("*")\
        .eq("id", catalog_id)\
        .execute()

    if not res.data:
        return {"error": "Not found"}

    return res.data[0]


# UPDATE
def update_catalog(catalog_id, data):

    supabase.table("drone_catalog")\
        .update(data)\
        .eq("id", catalog_id)\
        .execute()

    return {"message": "Catalog updated"}


# DELETE
def delete_catalog(catalog_id):

    supabase.table("drone_catalog")\
        .delete()\
        .eq("id", catalog_id)\
        .execute()

    return {"message": "Catalog deleted"}