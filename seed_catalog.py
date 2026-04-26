from app.db.supabase import supabase

def seed_catalog():

    data = [
        {
            "name": "SkyGuardian-V1",
            "model": "V1",
            "tagline": "High Altitude Surveillance",
            "price": 12400,

            "unit_id": "as-1",
            "system_auth": "VALID",
            "description": "Authorized hardware profile for series as-1. Optimized for high-altitude reconnaissance and encrypted data relay in hostile environments.",

            "encryption": "AES-256 Encrypted",
            "wind_resistance": "Up to 45km/h",

            "features": [
                "4K Thermal Night Vision",
                "60min Flight Time",
                "AI Face Recognition"
            ],

            "range": "25 KM / 15.5 MI",
            "link": "AES-256 ENCRYPTED",
            "sensors": "EO/IR QUAD-SENSOR",
            "wind": "UP TO 55 KM/H",

            "image_url": "https://images.unsplash.com/photo-1508614589041-895b88991e3e?q=80&w=800"
        },

        {
            "name": "Interceptor-X",
            "model": "X",
            "tagline": "Tactical Riot Control",
            "price": 18900,

            "unit_id": "as-2",
            "system_auth": "VALID",
            "description": "Authorized hardware profile for series as-2. Optimized for high-altitude reconnaissance and encrypted data relay in hostile environments.",

            "encryption": "Sat-Link Enabled",
            "wind_resistance": "Up to 55km/h",

            "features": [
                "Acoustic Hailer (Loudspeaker)",
                "Non-Lethal Deployment",
                "Object Tracking"
            ],

            "range": "25 KM / 15.5 MI",
            "link": "AES-256 ENCRYPTED",
            "sensors": "EO/IR QUAD-SENSOR",
            "wind": "UP TO 55 KM/H",

            "image_url": "https://images.pexels.com/photos/1087180/pexels-photo-1087180.jpeg?auto=compress&cs=tinysrgb&w=800"
        },

        {
            "name": "Specter-M7",
            "model": "M7",
            "tagline": "Stealth Reconnaissance",
            "price": 24500,

            "unit_id": "as-3",
            "system_auth": "VALID",
            "description": "Authorized hardware profile for series as-3. Optimized for high-altitude reconnaissance and encrypted data relay in hostile environments.",

            "encryption": "Military Grade",
            "wind_resistance": "Up to 40km/h",

            "features": [
                "Silent Propulsion System",
                "Multi-Target Radar",
                "BVLOS Operations"
            ],

            "range": "25 KM / 15.5 MI",
            "link": "AES-256 ENCRYPTED",
            "sensors": "EO/IR QUAD-SENSOR",
            "wind": "UP TO 55 KM/H",

            "image_url": "https://images.unsplash.com/photo-1508614589041-895b88991e3e?q=80&w=800"
        }
    ]

    res = supabase.table("drone_catalog").insert(data).execute()

    print("Inserted:", res.data)


if __name__ == "__main__":
    seed_catalog()