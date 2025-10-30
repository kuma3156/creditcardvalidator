from fastapi import FastAPI
from app.api.routes import router

def create_credit_validator() -> FastAPI:
    app = FastAPI(
        title="Credit Card Validator API",
        description="An API to validate credit card numbers using the Luhn algorithm.",
        version="1.0.0"
    )

    @app.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "ok"}
    
    app.include_router(router, prefix="/api")
    return app

app = create_credit_validator()