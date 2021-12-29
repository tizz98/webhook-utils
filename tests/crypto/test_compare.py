import pytest

from webhook_utils.crypto import (
    compare_md5_signature,
    compare_sha1_signature,
    compare_sha256_signature,
)


class TestCompareSignature:
    @pytest.mark.parametrize(
        "compare_fn,expected",
        [
            (compare_md5_signature, "78d6997b1230f38e59b6d1642dfaa3a4"),
            (compare_sha1_signature, "03376ee7ad7bbfceee98660439a4d8b125122a5a"),
            (
                compare_sha256_signature,
                "734cc62f32841568f45715aeb9f4d7891324e6d948e4c6c60c0621cdac48623a",
            ),
        ],
        ids=["md5", "sha1", "sha256"],
    )
    def test_compare_signature_methods_success(self, compare_fn, expected):
        assert compare_fn(b"secret", b"hello world", expected)

    @pytest.mark.parametrize(
        "compare_fn,expected",
        [
            (compare_md5_signature, "78d6997b1230f38e59b6d1642dfaa3a5"),
            (compare_sha1_signature, "03376ee7ad7bbfceee98660439a4d8b125122a6"),
            (
                compare_sha256_signature,
                "734cc62f32841568f45715aeb9f4d7891324e6d948e4c6c60c0621cdac48623b",
            ),
        ],
        ids=["md5", "sha1", "sha256"],
    )
    def test_compare_signature_methods_fail(self, compare_fn, expected):
        assert not compare_fn(b"secret", b"hello world", expected)
