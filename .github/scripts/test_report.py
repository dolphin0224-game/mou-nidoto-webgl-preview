import unittest
import report


class WebhookConfigurationTests(unittest.TestCase):
    endpoint = "https://discord.com/api/webhooks/123456789012345678/EXAMPLE_not_a_real_token"

    def test_copy_formats_resolve_to_same_discord_endpoint(self):
        for value in (self.endpoint, " \n" + self.endpoint + "\r\n", self.endpoint + "/",
                      self.endpoint.replace("discord.com", "discordapp.com"),
                      self.endpoint.replace("/api/", "/api/v10/"), self.endpoint + "/github"):
            with self.subTest(value=value):
                self.assertEqual(report.webhook_url(value), self.endpoint)

    def test_rejects_unrelated_or_malformed_destinations_without_echoing_value(self):
        for value in ("", "DISCORD_WEBHOOK_URL", "https://example.com/secret-value",
                      self.endpoint.replace("https:", "http:"),
                      self.endpoint.replace("discord.com", "discord.com.evil.test"),
                      self.endpoint + "?thread_id=secret-value", "https://discord.com/api/webhooks/123"):
            with self.subTest(value=value):
                with self.assertRaises(report.WebhookConfigurationError) as caught:
                    report.webhook_url(value)
                self.assertNotIn("secret-value", str(caught.exception))
                self.assertNotIn("EXAMPLE_not_a_real_token", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
