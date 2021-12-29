# Webhook Utils

A set of utilities for interacting with webhooks.

[![Test Webhook Utils](https://github.com/tizz98/webhook-utils/actions/workflows/main.yaml/badge.svg?branch=main)](https://github.com/tizz98/webhook-utils/actions/workflows/main.yaml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](https://github.com/tizz98/py-paas/tree/main/LICENSE)

## Installation

```shell
pip install webhook-utils
```

## Usage

### Crypto

Available hash algorithms for all methods are:
- `md5` (not recommended)
- `sha1`
- `sha256` (recommended)

Learn more about HMAC signatures [here](https://webhooks.dev/docs/auth/#hmac).

#### Generating HMAC signatures

Bare usage:
```python
from webhook_utils.crypto import generate_sha256_signature

print(generate_sha256_signature(b'secret-key', b'some-message'))
```

#### Comparing HMAC signatures

Bare usage:
```python
from webhook_utils.crypto import compare_sha256_signature

is_valid_signature = compare_sha256_signature(
    b'secret-key',
    b'some-message',
    'expected-signature',
)
if not is_valid_signature:
    raise ValueError('Invalid signature')
```

### Httpx

`webhook-utils` has a built-in `httpx.Auth` class that can be used to
automatically sign requests made with an `httpx.Client`.

An `X-Webhook-Signature` header will be added to all `POST` requests.
The signature will be generated using the `webhook_key` and the
provided signature method (defaults to `sha256`).

The header, signature, and http methods can be customized by passing
the `header_name`, `gen_signature_method`, and `methods` keyword arguments.

```shell
pip install webhook-utils[httpx]
```

```python
import httpx
from webhook_utils.contrib.httpx_auth import WebhookAuth
from webhook_utils.crypto import generate_sha1_signature

# Basic usage
auth = WebhookAuth("secret-key")
client = httpx.Client(auth=auth)


# Customized usage
auth = WebhookAuth(
    "secret-key",
    header_name="My-Webhook-Signature",
    gen_signature_method=generate_sha1_signature,
    methods={"POST", "PUT"},
)
client = httpx.Client(auth=auth)
client.post("https://example.com/webhook", json={"foo": "bar"})
```

## Publishing to PYPI

```shell
poetry build
# Verify that everything looks correct on test.pypi.org
poetry publish -r testpypi
poetry publish
```
