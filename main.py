from fastapi import FastAPI, Query, Body
import uvicorn
from hotels import router as router_hotels
app = FastAPI()

app.include_router(router_hotels, tags=["Отели"])


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
