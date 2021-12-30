from fastapi import APIRouter, FastAPI
from rich import print

from webhook_utils.contrib.fastapi import WebhookRouter

app = FastAPI(title="FastAPI Webhook Receiver")

# Create a router for the webhooks,
# validating the payloads with the given key.
webhook_router = WebhookRouter(
    APIRouter(prefix="/webhooks"),
    webhook_key="secret",
)


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


@webhook_router.on("/demo")
def demo_webhook(payload: dict):
    """Receive a webhook payload and print it to the console."""
    print(f"Received webhook payload: {payload}")


app.include_router(webhook_router.api_router)
