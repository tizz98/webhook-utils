from typing import Callable

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.types import DecoratedCallable

from webhook_utils.crypto import compare_sha256_signature


class WebhookRouter:
    """Wraps a FastAPI router and adds a signature verification step for webhooks.

    Example
    -------
    >>> from fastapi import FastAPI, APIRouter
    >>> app = FastAPI()
    >>> router = APIRouter(prefix="/webhooks")
    >>> webhook_router = WebhookRouter(router, webhook_key="secret")
    >>> @webhook_router.on("/demo-webhook")
    ... def demo_event_handler(request: Request):
    ...    return {"status": "ok"}
    >>> app.include_router(webhook_router.api_router)
    """

    def __init__(
        self,
        api_router: APIRouter,
        *,
        webhook_key: str,
        header_name: str = "X-Webhook-Signature",
        compare_signature_fn: Callable[
            [bytes, bytes, str], bool
        ] = compare_sha256_signature,
    ) -> None:
        """Initialize the WebhookRouter.

        Parameters
        ----------
        api_router: APIRouter
            The FastAPI router to wrap.
        webhook_key: str
            The webhook key to use for signature verification.
        header_name: str
            The name of the header to use for signature verification.
            Defaults to "X-Webhook-Signature".
        compare_signature_fn: Callable[[bytes, bytes, str], bool]
            The function to use for signature verification.
            Can be overridden for different signature algorithms.
            Defaults to `compare_sha256_signature`.
        """

        self._api_router = api_router
        self._webhook_key = webhook_key.encode("utf-8")
        self._header_name = header_name
        self._compare_signature_fn = compare_signature_fn

        self._api_router.dependencies.append(Depends(self._validate_webhook_signature))

    @property
    def api_router(self) -> APIRouter:
        """Returns the internal FastAPI router."""
        return self._api_router

    def on(self, *args, **kwargs) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """Adds an API route to the internal api router for this webhook event.

        Parameters are the same as the `APIRouter.api_route` decorator.
        The default HTTP method is `POST` and is generally recommended to use.
        """

        kwargs.setdefault("methods", ["POST"])

        def decorator(fn: DecoratedCallable) -> DecoratedCallable:
            return self._api_router.api_route(*args, **kwargs)(fn)

        return decorator

    async def _validate_webhook_signature(self, request: Request) -> None:
        """Check if the webhook signature is valid.

        This method is automatically added as a dependency to all routes
        created with `WebhookRouter.on`.

        Raises HTTPException (401) if the signature is invalid.
        Raise HTTPException (403) if the signature is not set.
        """

        signature = request.headers.get(self._header_name)
        if not signature:
            raise HTTPException(status_code=403, detail="Signature not set")
        if not self._compare_signature_fn(
            self._webhook_key, await request.body(), signature
        ):
            raise HTTPException(status_code=401, detail="Invalid signature")
