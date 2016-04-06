import os
from api.tests import base
from api.handlers.security import _is_valid_rsa_key, PUBLIC_KEY_FILE_NAME


class TestSecurity(base.BaseTestCase):

    _test_key = "-----BEGIN PUBLIC KEY-----\n" \
                "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsL8Q3GivUhjK0ia7S+VF\n" \
                "IwD5iJdcgxZFNrCCXeNtak2FpgHr9OvW/WyuwGF0TYh/2HvtX/dNhW3zBYr64nz3\n" \
                "dVkmu4aRjLf07LXutzbVv/n2DA1Xmok6vdZ5j6mRKdhAzsQxvBQxvgu7hRMAiJbg\n" \
                "o615P3EJkPTWgZpHNvlkIJFvMJy5iFpcPg+HXAmMPsvIA9h4ATPkfqXFxjPwwJTi\n" \
                "xHv19bfGKzjVJncZT3m1/0CQYUXZZxEq8Z9lOWQR9oEiG9Zd4n2K7Mvza3d5QWTs\n" \
                "LqNb2QcAIpRP8mKIoaAPZHwEWF5F0lYB6MusAneHFqsDx0cF+ZVUem1KXNMi+YTE\n" \
                "hQIDAQAB\n-----END PUBLIC KEY-----"

    def setUp(self):
        with open(PUBLIC_KEY_FILE_NAME, "w") as f:
            f.write(self._test_key)

    # GET /security/public_key

    def test_get_secret_key(self):
        status, body = self.get('/security/public_key')

        self.assertEqual(status, 200, msg=body.get("error", "Unhandled error."))

        self.assertTrue("key" in body)
        self.assertTrue(_is_valid_rsa_key(body["key"]))

    def test_get_does_not_exists(self):
        os.remove(PUBLIC_KEY_FILE_NAME)

        status, body = self.get('/security/public_key')

        self.assertEqual(status, 503, msg=body.get("error", "Unhandled error."))

    # POST /security/public_key

    def test_update_key(self):
        os.remove(PUBLIC_KEY_FILE_NAME)
        self.assertFalse(os.path.exists(PUBLIC_KEY_FILE_NAME))

        post_json = {"key": self._test_key}
        status, body = self.post('/security/public_key', post_json)

        self.assertEqual(status, 200, msg=body.get("error", "Unhandled error."))
        self.assertTrue(os.path.exists(PUBLIC_KEY_FILE_NAME))

    def test_update_invalid_key(self):
        post_json = {"key": "garbage_text"}
        status, body = self.post('/security/public_key', post_json)
        self.assertEqual(status, 400, msg=body.get("error", "Unhandled error."))

    def tearDown(self):
        if os.path.exists(PUBLIC_KEY_FILE_NAME):
            os.remove(PUBLIC_KEY_FILE_NAME)
