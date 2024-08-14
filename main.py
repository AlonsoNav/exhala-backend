from fastapi import FastAPI
from routes.user import user

app = FastAPI(
    title="Exhala back end",
)
app.include_router(user)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
