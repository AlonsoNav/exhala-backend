from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.user import user_router as user

app = FastAPI(
    title="Exhala back-end",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5137"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(user)
