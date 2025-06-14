from agno.tools import Toolkit
import whois
import dns.resolver
import socket
import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()

class DNSLookUp(Toolkit):

    def __init__(self, **kwargs):
        super().__init__(
            name="custom_tools",
            tools=[
                self.whois,
                self.get_mx_records,
                self.get_all_domain_ips,
                self.get_domain_geolocation,
                self.get_dns_records,
                self.detect_cdn_by_cname,
                self.reverse_dns_lookup,
                # self.check_brand_alert,
            ],
            **kwargs,
        )

    def whois(self, domain: str) -> str:
        """
        Perform a WHOIS lookup on the given domain.
        """
        print("Performing WHOIS lookup...")
        try:
            domain_info = whois.whois(domain)
            return str(domain_info)
        except Exception as e:
            return f"Error: {str(e)}"

    def get_dns_records(self, domain: str, record_type: str) -> list[str] | str:
        """
        Retrieve specified DNS records for a domain.

        Args:
            domain (str): The domain name to query.
            record_type (str): The DNS record type (e.g., A, MX, TXT, NS, CNAME, etc.).

        Returns:
            list[str]: A list of DNS records as strings.
            str: An error message if something goes wrong.
        """
        try:
            answers = dns.resolver.resolve(domain, record_type)
            return [rdata.to_text() for rdata in answers]
        except dns.resolver.NoAnswer:
            return f"No {record_type} records found for {domain}."
        except dns.resolver.NXDOMAIN:
            return f"Domain {domain} does not exist."
        except dns.resolver.NoNameservers:
            return f"No nameservers found for {domain}."
        except Exception as e:
            return f"Error retrieving {record_type} records: {e}"

    def get_mx_records(self, domain: str) -> list[dict] | str:
        """
        Retrieve MX (Mail Exchange) records for a given domain.

        MX records indicate the mail servers responsible for receiving email on behalf
        of the domain. Each record has a priority (lower number = higher priority) and
        a mail server hostname.

        Args:
            domain (str): The domain name to query (e.g., "example.com").

        Returns:
            list[dict]: A list of dictionaries containing 'priority' and 'mail_server'
                        for each MX record found.
            str: An error message if the domain is invalid or no records are found.

        Example:
            >>> get_mx_records("example.com")
            [
                {'priority': 10, 'mail_server': 'mail1.example.com.'},
                {'priority': 20, 'mail_server': 'mail2.example.com.'}
            ]
        """
        try:
            # Query MX records using dnspython
            answers = dns.resolver.resolve(domain, 'MX')
            mx_records = []

            for rdata in answers:
                mx_records.append({
                    'priority': rdata.preference,
                    'mail_server': str(rdata.exchange)
                })

            return mx_records

        except dns.resolver.NoAnswer:
            return f"No MX records found for domain: {domain}"
        except dns.resolver.NXDOMAIN:
            return f"Domain does not exist: {domain}"
        except dns.resolver.Timeout:
            return f"DNS query timed out for domain: {domain}"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def get_all_domain_ips(self, domain: str) -> dict:
        """
        Get all IPv4 (A) and IPv6 (AAAA) addresses for a domain.

        Args:
            domain (str): The domain name.

        Returns:
            dict: A dictionary with keys 'A' and 'AAAA' and their respective IP lists.
        """
        ip_info = {'A': [], 'AAAA': []}

        try:
            a_records = dns.resolver.resolve(domain, 'A')
            ip_info['A'] = [rdata.to_text() for rdata in a_records]
        except dns.resolver.NoAnswer:
            ip_info['A'] = ["No A record found."]
        except Exception as e:
            ip_info['A'] = [f"Error: {e}"]

        try:
            aaaa_records = dns.resolver.resolve(domain, 'AAAA')
            ip_info['AAAA'] = [rdata.to_text() for rdata in aaaa_records]
        except dns.resolver.NoAnswer:
            ip_info['AAAA'] = ["No AAAA record found."]
        except Exception as e:
            ip_info['AAAA'] = [f"Error: {e}"]

        return ip_info


    def reverse_dns_lookup(ip: str) -> str:
        """
        Perform reverse DNS lookup to find the domain name associated with an IP address.

        Args:
            ip (str): IP address to look up.

        Returns:
            str: Resolved domain name or error message.
        """
        try:
            domain_name = socket.gethostbyaddr(ip)
            return f"Reverse DNS: {domain_name[0]}"
        except socket.herror:
            return "No PTR record found or IP not mapped to any hostname."
        

    def get_domain_geolocation(self, ip: str) -> dict | str:
        """
        Get geolocation data for a given ip.

        Args:
            ip (str): The ip of the domain  (e.g., '160.153.0.113').

        Returns:
            dict: A dictionary containing geolocation info (country, city, ISP, etc.).
            str: Error message if something fails.
        """
        print("Performing geolocation lookup...", ip)

        try:
            # Resolve domain to IP address
            # ip = socket.gethostbyname(domain)

            # Call IP geolocation API
            response = requests.get(f"http://ip-api.com/json/{ip}")
            data = response.json()

            if data['status'] == 'success':
                return {
                    'ip': ip,
                    'country': data['country'],
                    'region': data['regionName'],
                    'city': data['city'],
                    'zip': data['zip'],
                    'lat': data['lat'],
                    'lon': data['lon'],
                    'timezone': data['timezone'],
                    'isp': data['isp'],
                    'org': data['org']
                }
            else:
                return f"API error: {data['message']}"
        except Exception as e:
            return f"Error: {e}"

    def detect_cdn_by_cname(self, domain: str) -> str:
        """
        Attempts to detect CDN usage by inspecting CNAME records.

        Args:
            domain (str): The domain name.

        Returns:
            str: CDN provider name or a message saying not detected.
        """
        cdn_signatures = {
            "cloudflare": "cdn.cloudflare.net",
            "akamai": "akamaiedge.net",
            "cloudfront": "cloudfront.net",
            "fastly": "fastly.net",
            "google": "googleusercontent.com",
            "azure": "azureedge.net",
            "stackpath": "stackpathdns.com",
            "limelight": "llnwd.net",
            "bunnycdn": "b-cdn.net"
        }

        try:
            answers = dns.resolver.resolve(domain, 'CNAME')
            for rdata in answers:
                target = rdata.target.to_text().lower()
                for cdn, signature in cdn_signatures.items():
                    if signature in target:
                        return f"CDN Detected: {cdn.capitalize()} ({signature})"
            return "No known CDN detected via CNAME."
        except dns.resolver.NoAnswer:
            return "No CNAME record (likely A record used)."
        except Exception as e:
            return f"Error: {e}"
        

    def check_brand_alert(self, domain: str,  with_typos: bool = True) -> dict:
        """
        Query the WHOISXML Brand Alert API to find similar or typosquatted domains
        related to the provided domain name.

        Args:
            domain (str): The base domain to monitor (e.g., "google.com").
            with_typos (bool): Whether to include typosquatting variants. Default is True.

        Returns:
            dict: JSON response from the API containing potentially related domains.
        """
        # Extract keyword from domain (e.g., "google" from "google.com")
        keyword = domain

        # Use yesterday's date since the API fetches data from yesterday
        # since_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
        api_key = os.getenv("WHOIS_API_KEY")
        url = "https://brand-alert.whoisxmlapi.com/api/v2"
        payload = {
            "apiKey": api_key,
            "mode": "purchase",
            "withTypos": with_typos,
            "responseFormat": "json",
            "punycode": True,
            "includeSearchTerms": [keyword]
        }

        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            print("Brand Alert API response:", response.json())
            return  response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
