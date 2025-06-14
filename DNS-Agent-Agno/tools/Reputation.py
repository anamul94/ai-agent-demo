from agno.tools import Toolkit
import requests
import os

class Reputation(Toolkit):
    """
    A class to perform various reputation checks on a given domain.
    """

    def __init__(self, **kwargs):
        super().__init__(
            name="custom_tools",
            tools=[
                self.check_google_safe_browsing,
            ],
            **kwargs,
        )

    def check_google_safe_browsing(self, domain: str, api_key: str) -> str:
        """
        Check if a domain is listed in Google's Safe Browsing threat list.

        Args:
            domain (str): The domain to check.
            api_key (str): Your Google Safe Browsing API key.

        Returns:
            str: 'Safe' or threat info.
        """
        url = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=" + api_key
        payload = {
            "client": {"clientId": "yourcompanyname", "clientVersion": "1.0"},
            "threatInfo": {
                "threatTypes": [
                    "MALWARE",
                    "SOCIAL_ENGINEERING",
                    "UNWANTED_SOFTWARE",
                    "POTENTIALLY_HARMFUL_APPLICATION",
                ],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": f"http://{domain}/"}],
            },
        }

        response = requests.post(url, json=payload)
        data = response.json()

        if "matches" in data:
            return f"⚠️ Threat detected: {data['matches']}"
        return "✅ Domain is clean according to Google Safe Browsing."


# Example
# api_key = "YOUR_API_KEY"
# print(check_google_safe_browsing("example.com", api_key))
