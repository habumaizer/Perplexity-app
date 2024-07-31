from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from API.api_router import router as api_router
from API.root_router import root_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(root_router)

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
