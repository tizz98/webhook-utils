# Webhook Utils

A set of utilities for interacting with webhooks.

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
