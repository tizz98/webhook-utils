import httpx
import pytest

from webhook_utils.contrib.httpx_auth import WebhookAuth
from webhook_utils.crypto import generate_sha1_signature


class TestWebhookAuth:
    @pytest.fixture
    def webhook_auth(self):
        return WebhookAuth("secret")

    @pytest.fixture
    def httpx_client(self, webhook_auth):
        return httpx.Client(auth=webhook_auth)

    def test_webhook_body_is_signed(self, httpx_client, respx_mock):
        expected_signature = "aebddf851b0db5f85a3a9da22228ef96fdb124d0251cd48d4fc0f3d08c1a79b4"  # noqa: E501
        route = respx_mock.post(
            "https://example.com/webhook",
            headers={"X-Webhook-Signature": expected_signature},
            json={"foo": "bar"},
        ).mock(return_value=httpx.Response(200))
        response = httpx_client.post("https://example.com/webhook", json={"foo": "bar"})
        assert response.status_code == 200
        assert route.called

    @pytest.mark.parametrize(
        "method", ["get", "put", "delete", "head", "options", "patch"]
    )
    def test_webhook_body_is_not_signed_for_unspecified_methods(
        self, httpx_client, respx_mock, method
    ):
        route = respx_mock.route(
            url="https://example.com/webhook", method=method, headers={}
        ).mock(return_value=httpx.Response(200))
        response = getattr(httpx_client, method)("https://example.com/webhook")
        assert response.status_code == 200
        assert route.called

    def test_custom_header_name_is_used(self, httpx_client, webhook_auth, respx_mock):
        webhook_auth.header_name = "X-Hub-Signature"
        expected_signature = "aebddf851b0db5f85a3a9da22228ef96fdb124d0251cd48d4fc0f3d08c1a79b4"  # noqa: E501
        route = respx_mock.post(
            "https://example.com/webhook",
            headers={"X-Hub-Signature": expected_signature},
            json={"foo": "bar"},
        ).mock(return_value=httpx.Response(200))
        response = httpx_client.post("https://example.com/webhook", json={"foo": "bar"})
        assert response.status_code == 200
        assert route.called

    def test_custom_methods_are_supported(self, httpx_client, webhook_auth, respx_mock):
        webhook_auth.methods = {"PUT"}
        expected_signature = "aebddf851b0db5f85a3a9da22228ef96fdb124d0251cd48d4fc0f3d08c1a79b4"  # noqa: E501
        route = respx_mock.put(
            "https://example.com/webhook",
            headers={"X-Webhook-Signature": expected_signature},
            json={"foo": "bar"},
        ).mock(return_value=httpx.Response(200))
        response = httpx_client.put("https://example.com/webhook", json={"foo": "bar"})
        assert response.status_code == 200
        assert route.called

    def test_custom_signature_methods_are_supported(
        self, httpx_client, webhook_auth, respx_mock
    ):
        webhook_auth.gen_signature_method = generate_sha1_signature
        expected_signature = "cf1968b0954f5078512814c983937bb3227047e1"
        route = respx_mock.post(
            "https://example.com/webhook",
            headers={"X-Webhook-Signature": expected_signature},
            json={"foo": "bar"},
        ).mock(return_value=httpx.Response(200))
        response = httpx_client.post("https://example.com/webhook", json={"foo": "bar"})
        assert response.status_code == 200
        assert route.called
