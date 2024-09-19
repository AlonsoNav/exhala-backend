from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user import user_router as user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5137"],  # Update when deploying
    allow_credentials=True,  # Allow tokens and cookies
    allow_methods=["*"],  # Restrict methods when deploying
    allow_headers=["*"],
)

# Routes
app.include_router(user)
