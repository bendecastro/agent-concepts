import unittest

from users import handlers, store


class HandlerTests(unittest.TestCase):
    def setUp(self):
        store.add_user(1, "Ada", "ada@example.com")

    def test_show_user(self):
        self.assertEqual(handlers.show_user(1)["name"], "Ada")

    def test_change_email(self):
        handlers.change_email(1, "new@example.com")
        self.assertEqual(handlers.show_user(1)["email"], "new@example.com")


if __name__ == "__main__":
    unittest.main()
