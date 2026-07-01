from fastapi import FastAPI

app = FastAPI(
    title="Fair & Fast Python API Template",
    version="1.0.0",
    description="Standard FastAPI template for Fair & Fast projects"
)

@app.get("/")
def root():
    return {
        "service": "Fair & Fast Python API Template",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }
