from dnstwist import dnstwist


def find_typosquatted_domains(domain: str):
    """
    Generate and check for typosquatted domains using dnstwist.

    Args:
        domain (str): The base domain to generate variants for.

    Returns:
        list: A list of detected domains that are registered.
    """
    scanner = dnstwist.DNSTwist(domain)
    results = scanner.run()
    active_domains = []

    for result in results:
        if result.get("dns-a") or result.get("dns-ns"):
            active_domains.append(result["domain"])

    return active_domains


# Example
print(find_typosquatted_domains("google.com"))
