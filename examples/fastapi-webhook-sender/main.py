import httpx
from fastapi import FastAPI

from webhook_utils.contrib.httpx_auth import WebhookAuth

app = FastAPI(title="FastAPI Webhook Sender")

# httpx.Client with WebhookAuth to automatically sign requests.
webhook_client = httpx.Client(
    auth=WebhookAuth(webhook_key="secret"), base_url="http://localhost:8000/webhooks"
)


@app.post("/demo")
def send_demo_webhook(payload: dict):
    """Send a demo webhook to fastapi-webhook-receiver."""

    resp = webhook_client.post("/demo", json=payload)
    resp.raise_for_status()
    return {"status": "ok"}
