import typing

import httpx
from httpx import Request, Response

from webhook_utils.crypto import generate_sha256_signature


class WebhookAuth(httpx.Auth):
    """Custom httpx.Auth class for Webhooks.

    Based on the webhook key and header provided, this class
    will inject a header with the signature of request body.

    Example
    -------
    >>> from webhook_utils.contrib.httpx_auth import WebhookAuth
    >>> client = httpx.Client(auth=WebhookAuth("secret", ""))
    >>> client.post("https://example.com/webhook", json={"foo": "bar"})
    """

    requires_request_body = True

    def __init__(
        self,
        webhook_key: str,
        *,
        header_name: str = "X-Webhook-Signature",
        gen_signature_method=generate_sha256_signature,
        methods: typing.Set[str] = frozenset({"POST"}),
    ) -> None:
        """Initialize the WebhookAuth class.

        Parameters
        ----------
        webhook_key : str
            The webhook key.
        header_name : str, optional
            The name of the header to be injected. Defaults to "X-Webhook-Signature".
        gen_signature_method : function, optional
            The function to generate the signature. Defaults to
            `generate_sha256_signature`.
        methods : set, optional
            The methods to be signed. Defaults to {"POST"}.
        """
        self.webhook_key = webhook_key.encode("utf-8")
        self.header_name = header_name
        self.gen_signature_method = gen_signature_method
        self.methods = methods

    def auth_flow(self, request: Request) -> typing.Generator[Request, Response, None]:
        """Generate signature and inject header.

        Parameters
        ----------
        request : Request
            The request to be signed.

        Yields
        ------
        Request
            The signed request.
        """

        if request.method in self.methods:
            signature = self.gen_signature_method(request.content, self.webhook_key)
            print(signature)
            request.headers[self.header_name] = signature

        yield request
