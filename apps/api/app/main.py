from fastapi import FastAPI

app = FastAPI(
    title="Eidos API",
    version="0.1.0",
    summary="Local-first orchestration layer for portfolio intelligence",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
