from fastapi import FastAPI
from routes.webhook_routes import webhook_router
from routes.index_repo_dev_only import dev_router

app = FastAPI()

app.include_router(webhook_router, prefix="/api/v1/webhooks",tags=["Webhook"])
app.include_router(dev_router, prefix="/api/v1/dev",tags=["Dev"])

@app.get('/')
def greet():
    return {"status" : "server working"}

