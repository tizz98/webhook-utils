import pytest
from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

from webhook_utils.contrib.fastapi import WebhookRouter
from webhook_utils.crypto import (
    compare_sha1_signature,
    generate_sha1_signature,
    generate_sha256_signature,
)


class TestWebhookRouter:
    @pytest.fixture
    def webhook_router(self):
        return WebhookRouter(APIRouter(prefix="/webhooks"), webhook_key="secret")

    @pytest.fixture
    def app(self, webhook_router):
        app = FastAPI()

        @webhook_router.on("/demo-webhook")
        def demo_webhook():
            return {"message": "Hello!"}

        app.include_router(webhook_router.api_router)
        return app

    @pytest.fixture
    def client(self, app):
        return TestClient(app)

    def test_403_when_no_signature(self, client):
        response = client.post("/webhooks/demo-webhook", json={"foo": "bar"})
        assert response.status_code == 403

    def test_401_when_invalid_signature(self, client):
        response = client.post(
            "/webhooks/demo-webhook",
            headers={"X-Webhook-Signature": "invalid"},
            json={"foo": "bar"},
        )
        assert response.status_code == 401

    def test_200_when_valid_signature(self, client):
        expected_signature = generate_sha256_signature(b"secret", b'{"foo": "bar"}')
        response = client.post(
            "/webhooks/demo-webhook",
            headers={"X-Webhook-Signature": expected_signature},
            json={"foo": "bar"},
        )
        assert response.status_code == 200

    def test_header_can_be_overridden(self, client, webhook_router):
        webhook_router._header_name = "X-Hub-Signature"
        expected_signature = generate_sha256_signature(b"secret", b'{"foo": "bar"}')
        response = client.post(
            "/webhooks/demo-webhook",
            headers={"X-Hub-Signature": expected_signature},
            json={"foo": "bar"},
        )
        assert response.status_code == 200

    def test_signature_function_can_be_overridden(self, client, webhook_router):
        webhook_router._compare_signature_fn = compare_sha1_signature
        expected_signature = generate_sha1_signature(b"secret", b'{"foo": "bar"}')
        response = client.post(
            "/webhooks/demo-webhook",
            headers={"X-Webhook-Signature": expected_signature},
            json={"foo": "bar"},
        )
        assert response.status_code == 200
