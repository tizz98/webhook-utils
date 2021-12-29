import pytest

from webhook_utils.crypto import (
    generate_md5_signature,
    generate_sha1_signature,
    generate_sha256_signature,
)


class TestGenerateSignature:
    @pytest.mark.parametrize(
        "generate_fn, expected",
        [
            (generate_md5_signature, "78d6997b1230f38e59b6d1642dfaa3a4"),
            (generate_sha1_signature, "03376ee7ad7bbfceee98660439a4d8b125122a5a"),
            (
                generate_sha256_signature,
                "734cc62f32841568f45715aeb9f4d7891324e6d948e4c6c60c0621cdac48623a",
            ),
        ],
        ids=["md5", "sha1", "sha256"],
    )
    def test_generate_signature(self, generate_fn, expected):
        assert generate_fn(b"secret", b"hello world") == expected

    @pytest.mark.parametrize(
        "generate_fn",
        [
            generate_md5_signature,
            generate_sha1_signature,
            generate_sha256_signature,
        ],
        ids=["md5", "sha1", "sha256"],
    )
    def test_generate_signature_different_values_are_not_equal(self, generate_fn):
        assert generate_fn(b"secret", b"hello world") != generate_fn(
            b"secret", b"hello world!"
        )
