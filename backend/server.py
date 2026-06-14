from fastapi import FastAPI
from routes.webhook_routes import webhook_router

app = FastAPI()

app.include_router(webhook_router, prefix="/api/v1/webhooks",tags=["Webhook"])

@app.get('/')
def greet():
    return {"status" : "server working"}

