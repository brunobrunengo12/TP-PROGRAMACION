from fastapi import FastAPI
from routers import libros, users

app = FastAPI()

app.include_router(users.router)
app.include_router(libros.router)


@app.get("/")
def read_root():
    mensaje = "Primer clase de FastAPI"
    return {"message": mensaje}