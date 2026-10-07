from fastapi import FastAPI

app = FastAPI(
    title="Designex AI Studio",
    description="AI intelligence layer for Designex project, visual and content workflows.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "Designex AI Studio",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }