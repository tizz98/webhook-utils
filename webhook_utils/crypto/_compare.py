"""Functions for comparing HMAC digests."""
import hashlib
import hmac
from functools import partial


def compare_signature(
    digestmod, key: bytes, message: bytes, expected_signature: str
) -> bool:
    """Compare the HMAC signature of a message with an expected signature."""
    mac = hmac.new(key, message, digestmod)
    return hmac.compare_digest(mac.hexdigest(), expected_signature)


compare_md5_signature = partial(compare_signature, hashlib.md5)
compare_sha1_signature = partial(compare_signature, hashlib.sha1)
compare_sha256_signature = partial(compare_signature, hashlib.sha256)
