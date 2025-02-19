from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user import user_router as user
from routes.psychologist import psychologist_router as psychologist
import requests
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Update when deploying
    allow_credentials=True,  # Allow tokens and cookies
    allow_methods=["*"],  # Restrict methods when deploying
    allow_headers=["*"],
)

# Routes
app.include_router(user)
app.include_router(psychologist)

@app.get("/my-ip")
def get_ip():
    ip = requests.get("https://api64.ipify.org?format=json").json()["ip"]
    return {"server_ip": ip}