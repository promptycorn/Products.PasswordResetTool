from email.header import decode_header
import unittest

from Products.PasswordResetTool.browser import PasswordResetToolView


class MailHeaderTests(unittest.TestCase):
    def test_non_ascii_sender_is_rfc2047_encoded(self):
        text = 'Old\u0159ich a Bo\u017eena'
        view = PasswordResetToolView(None, None)
        encoded = view.encode_mail_header(text)
        self.assertIsInstance(encoded, str)
        self.assertTrue(encoded.isascii())
        chunks = decode_header(encoded)
        self.assertEqual(''.join(value.decode(charset or 'ascii') if isinstance(value, bytes)
                                 else value for value, charset in chunks), text)

    def test_utf8_input_is_accepted(self):
        view = PasswordResetToolView(None, None)
        self.assertEqual(view.encode_mail_header('Gr\u00fc\u00dfe'.encode('utf-8')),
                         view.encode_mail_header('Gr\u00fc\u00dfe'))
