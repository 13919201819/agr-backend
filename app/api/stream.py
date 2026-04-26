from fastapi import APIRouter
from app.db.supabase import supabase
from app.services import stream_manager
from app.services.stream_service import start_camera, stop_camera
from datetime import datetime

router = APIRouter()

@router.post("/start")
def start_stream(data: dict):
    drone_id = data["drone_id"]
    stream_url = data["stream_url"]

    # Convert to int if webcam index
    if str(stream_url).isdigit():
        stream_url = int(stream_url)

    drone_res = supabase.table("drones").select("*").eq("id", drone_id).execute()
    if not drone_res.data:
        return {"error": "Invalid drone_id"}
    drone = drone_res.data[0]

    # Check if already running
    if stream_manager.camera_running:
        return {"error": "A stream is already running. Stop it first."}

    stream_res = supabase.table("streams").insert({
        "drone_id": drone_id,
        "stream_url": str(stream_url),
        "status": "active",
        "started_at": datetime.utcnow().isoformat()
    }).execute()

    stream = stream_res.data[0]
    stream_id = stream["id"]

    stream_manager.active_streams[stream_id] = True

    # ✅ Start single camera thread
    start_camera(stream_url, stream_id)

    return {
        "message": "Stream started",
        "stream": {
            "id": stream_id,
            "status": stream["status"],
            "stream_url": stream["stream_url"],
            "started_at": stream["started_at"],
            "drone": {
                "id": drone["id"],
                "name": drone.get("name"),
                "model": drone.get("model"),
                "tenant_id": drone.get("tenant_id")
            }
        }
    }


@router.post("/stop")
def stop_stream(data: dict):
    stream_id = data["stream_id"]

    if stream_id not in stream_manager.active_streams:
        return {"error": "Stream not running"}

    # ✅ Stop camera first
    stop_camera()

    # ✅ Update DB safely
    try:
        supabase.table("streams").update({
            "status": "stopped"
        }).eq("id", stream_id).execute()
    except Exception as e:
        print(f"⚠️ DB update failed: {e}")

    return {"message": f"Stream {stream_id} stopped successfully"}