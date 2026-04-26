from fastapi import FastAPI
from app.api import auth, drones, dashboard
from app.api import test
from app.api import auth
from app.api import users
from app.api import procurement
from app.api import catalog
from app.api import stream, websocket
from app.api import video
from app.api import logs





app = FastAPI(title="Agrani Backend")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(drones.router, prefix="/drones", tags=["Drones"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(test.router)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(procurement.router, prefix="/procurement", tags=["Procurement"])
app.include_router(catalog.router, prefix="/catalog", tags=["Catalog"])
app.include_router(stream.router, prefix="/stream", tags=["Stream"])
app.include_router(websocket.router)
app.include_router(video.router, prefix="/stream", tags=["Video"])
app.include_router(logs.router, prefix="/logs", tags=["Logs"])

@app.get("/")
def root():
    return {"message": "Agrani Backend Running"}