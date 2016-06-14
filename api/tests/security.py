import os
from flask import current_app as app

from api.tests import base


class TestSecurity(base.BaseTestCase):

    _test_key = "-----BEGIN PUBLIC KEY-----\n" \
                "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsL8Q3GivUhjK0ia7S+VF\n" \
                "IwD5iJdcgxZFNrCCXeNtak2FpgHr9OvW/WyuwGF0TYh/2HvtX/dNhW3zBYr64nz3\n" \
                "dVkmu4aRjLf07LXutzbVv/n2DA1Xmok6vdZ5j6mRKdhAzsQxvBQxvgu7hRMAiJbg\n" \
                "o615P3EJkPTWgZpHNvlkIJFvMJy5iFpcPg+HXAmMPsvIA9h4ATPkfqXFxjPwwJTi\n" \
                "xHv19bfGKzjVJncZT3m1/0CQYUXZZxEq8Z9lOWQR9oEiG9Zd4n2K7Mvza3d5QWTs\n" \
                "LqNb2QcAIpRP8mKIoaAPZHwEWF5F0lYB6MusAneHFqsDx0cF+ZVUem1KXNMi+YTE\n" \
                "hQIDAQAB\n-----END PUBLIC KEY-----"

    def create_public_key(self):
        with open(app.config["PUBLIC_KEY_FILE_NAME"], "w") as f:
            f.write(self._test_key)

    def tearDown(self):
        if os.path.exists(app.config["PUBLIC_KEY_FILE_NAME"]):
            os.remove(app.config["PUBLIC_KEY_FILE_NAME"])

    # GET /security/public_key

    def test_get_public_key(self):
        self.create_public_key()

        status, body = self.get('/security/public_key')

        self.assertEqual(status, 200)
        self.assertEqual(body['key'], self._test_key)

    def test_get_public_key_not_exists(self):
        status, body = self.get('/security/public_key')
        self.assertEqual(status, 503)

    # POST /security/public_key

    def test_update_public_key(self):
        self.assertFalse(os.path.exists(app.config["PUBLIC_KEY_FILE_NAME"]))

        status, body = self.post('/security/public_key', {"key": self._test_key}, token=self.get_system_token())

        self.assertEqual(status, 200)
        self.assertTrue(os.path.exists(app.config["PUBLIC_KEY_FILE_NAME"]))

    def test_update_public_key_overwrite(self):
        self.create_public_key()

        new_key = self._test_key.replace('5', '9')

        status, body = self.post('/security/public_key', {'key': new_key}, token=self.get_system_token())
        self.assertEqual(status, 200)

        status, body = self.get('/security/public_key')
        self.assertEqual(status, 200)
        self.assertEqual(body['key'], new_key)

    def test_update_public_key_error(self):
        status, body = self.post('/security/public_key', '', token=self.get_system_token())
        self.assertEqual(status, 400)

        status, body = self.post('/security/public_key', {"not_key": "123"}, token=self.get_system_token())
        self.assertEqual(status, 400)

        status, body = self.post('/security/public_key', {"key": "garbage_text"}, token=self.get_system_token())
        self.assertEqual(status, 400)
