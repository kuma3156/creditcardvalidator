from fastapi import FastAPI
from app.api.routes import router


## This generates the FastAPI application for the Credit Card Validator API.
def create_credit_validator() -> FastAPI:
    app = FastAPI(
        title="Credit Card Validator API",
        description="An API to validate credit card numbers using the Luhn algorithm.",
        version="1.0.0",
    )

    ##Create a health check endpoint to verify the service is running.
    @app.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "ok"}

    ## Include the router from the routes module to handle API requests.
    app.include_router(router, prefix="/api")
    return app


## Create the FastAPI app instance
app = create_credit_validator()
