"""Functions for generating hmac signatures of bytes."""
import hashlib
import hmac
from functools import partial


def generate_signature(digestmod, key: bytes, message: bytes) -> str:
    """Generate an HMAC signature for a message."""
    return hmac.new(key, message, digestmod).hexdigest()


generate_md5_signature = partial(generate_signature, hashlib.md5)
generate_sha1_signature = partial(generate_signature, hashlib.sha1)
generate_sha256_signature = partial(generate_signature, hashlib.sha256)
