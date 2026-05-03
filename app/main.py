# from fastapi import FastAPI
# from app.api import auth, drones, dashboard
# from app.api import test
# from app.api import users
# from app.api import procurement
# from app.api import catalog
# from app.api import stream, websocket
# from app.api import video
# from app.api import logs

# app = FastAPI(title="Agrani Backend")

# app.include_router(auth.router, prefix="/auth", tags=["Auth"])
# app.include_router(drones.router, prefix="/drones", tags=["Drones"])
# app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
# app.include_router(test.router)
# app.include_router(users.router, prefix="/users", tags=["Users"])
# app.include_router(procurement.router, prefix="/procurement", tags=["Procurement"])
# app.include_router(catalog.router, prefix="/catalog", tags=["Catalog"])
# app.include_router(stream.router, prefix="/stream", tags=["Stream"])
# app.include_router(websocket.router)
# app.include_router(video.router, prefix="/stream", tags=["Video"])
# app.include_router(logs.router, prefix="/logs", tags=["Logs"])

# @app.get("/")
# def root():
#     return {"message": "Agrani Backend Running"}



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 1. Import the middleware
from app.api import auth, drones, dashboard
from app.api import test
from app.api import users
from app.api import procurement
from app.api import catalog
from app.api import stream, websocket
from app.api import video
from app.api import logs

app = FastAPI(title="Agrani Backend")

# 2. Define the Origins (The domains allowed to talk to your backend)
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://13919201819.github.io", # <-- CHANGE THIS to your actual GitHub Pages URL
]

# 3. Add the Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Allows the origins defined above
    allow_credentials=True,         # Allows cookies/auth headers
    allow_methods=["*"],            # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],            # Allows all headers
)

# Your existing routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(drones.router, prefix="/drones", tags=["Drones"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(test.router)
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